#!/usr/bin/env python3
import argparse
import boto3
import json
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--thing", default="TrafficLightCloud",
                        help="Name of the AWS IOT thing")
    args = parser.parse_args()

    client = boto3.client("iot-data")

    states = [{"red": "on", "yellow": "off", "green": "off"},
              {"red": "off", "yellow": "on", "green": "off"},
              {"red": "off", "yellow": "off", "green": "on"}]

    for i in range(12):
        state = states[i % len(states)]
        shadow = {"state": {"desired": state} }
        payload = json.dumps(shadow).encode("utf-8")
        client.update_thing_shadow(thingName=args.thing, payload=payload)
        time.sleep(1)

if __name__ == "__main__":
    main()
