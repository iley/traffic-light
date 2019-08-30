#!/usr/bin/env python3
import argparse
import json
import time
import os

import boto3
import requests
from requests.auth import HTTPBasicAuth


def getenv(name):
    value = os.getenv(name)
    assert value, name + " env variable not set"
    return value


def lambda_handler(event, context):
    thing_name = getenv("IOT_THING")
    jenkins_url = getenv("JENKINS_URL")
    jenkins_job = getenv("JENKINS_JOB")
    jenkins_user = getenv("JENKINS_USER")
    jenkins_token = getenv("JENKINS_TOKEN")

    status = get_job_status(jenkins_url, jenkins_job, jenkins_user, jenkins_token)

    state = {"red": "off", "yellow": "off", "green": "off"}
    state[status] = "on"

    print("setting state to %s" % state)

    iot_client = boto3.client("iot-data")
    shadow = {"state": {"desired": state} }
    payload = json.dumps(shadow).encode("utf-8")
    iot_client.update_thing_shadow(thingName=thing_name, payload=payload)


# returns "red", "yellow" or "green"
def get_job_status(base_url, job, user, token):
    full_url = "%s/job/%s/lastBuild/api/json" % (base_url, job)
    resp = requests.get(full_url, auth=HTTPBasicAuth(user, token))

    if resp.status_code != requests.codes.ok:
        return "yellow"

    data = resp.json()
    result = data["result"]
    if result == "SUCCESS":
        return "green"
    else:
        return "red"


if __name__ == "__main__":
    lambda_handler(None, None)
