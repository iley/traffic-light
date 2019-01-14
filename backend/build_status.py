#!/usr/bin/env python3
import argparse
import json
import time
import os

import boto3
import requests
from requests.auth import HTTPBasicAuth


DEFAULT_THING = "TrafficLightCloud"
DEFAULT_BAMBOO_URL = "https://atlassian.aid-driving.eu/bamboo"
DEFAULT_PLAN = "AS-AS"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--thing", default=DEFAULT_THING, help="Name of the AWS IOT thing")
    parser.add_argument("--bamboo", default=DEFAULT_BAMBOO_URL, help="Bamboo URL")
    parser.add_argument("--plan", default=DEFAULT_PLAN, help="Bamboo build plan name")
    args = parser.parse_args()
    update_status(args.bamboo, args.plan, args.thing)


def lambda_handler(event, context):
    update_status(DEFAULT_BAMBOO_URL, DEFAULT_PLAN, DEFAULT_THING)


def update_status(bamboo_url, bamboo_plan, thing_name):
    atlassian_user = os.getenv("ATLASSIAN_USER")
    assert atlassian_user, "ATLASSIAN_USER not specified"
    atlassian_pass = os.getenv("ATLASSIAN_PASS")
    assert atlassian_pass, "ATLASSIAN_PASS not specified"

    auth = HTTPBasicAuth(atlassian_user, atlassian_pass)

    status = get_bamboo_status(bamboo_url, bamboo_plan, auth)
    print("last status is %s" % status)

    state = {"red": "off", "yellow": "off", "green": "off"}
    state[status] = "on"

    iot_client = boto3.client("iot-data")
    shadow = {"state": {"desired": state} }
    payload = json.dumps(shadow).encode("utf-8")
    iot_client.update_thing_shadow(thingName=thing_name, payload=payload)


# returns "red", "yellow" or "green"
def get_bamboo_status(base_url, plan, auth):
    full_url = "%s/rest/api/latest/result/%s.json" % (base_url, plan)
    resp = requests.get(full_url, auth=auth)
    resp.raise_for_status()
    data = resp.json()
    last_result = data["results"]["result"][0]
    if last_result["state"] == "Successful":
        return "green"
    elif last_result["buildState"] == "Successful":
        return "yellow"
    else:
        return "red"


if __name__ == "__main__":
    main()
