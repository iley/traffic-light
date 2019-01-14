#!/usr/bin/env python3
import argparse
import json
import time
import os

import boto3
import requests
from requests.auth import HTTPBasicAuth


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--thing", default="TrafficLightCloud",
                        help="Name of the AWS IOT thing")
    parser.add_argument("--bamboo", default="https://atlassian.aid-driving.eu/bamboo", help="Bamboo URL")
    parser.add_argument("--plan", default="AS-AS", help="Bamboo build plan name")
    args = parser.parse_args()

    atlassian_user = os.getenv("ATLASSIAN_USER")
    assert atlassian_user, "ATLASSIAN_USER not specified"
    atlassian_pass = os.getenv("ATLASSIAN_PASS")
    assert atlassian_pass, "ATLASSIAN_PASS not specified"

    auth = HTTPBasicAuth(atlassian_user, atlassian_pass)

    status = get_bamboo_status(args.bamboo, args.plan, auth)
    print("last status is %s" % status)

    state = {"red": "off", "yellow": "off", "green": "off"}
    state[status] = "on"

    iot_client = boto3.client("iot-data")
    shadow = {"state": {"desired": state} }
    payload = json.dumps(shadow).encode("utf-8")
    iot_client.update_thing_shadow(thingName=args.thing, payload=payload)


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
