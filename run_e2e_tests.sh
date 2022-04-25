#!/usr/bin/env bash

docker run --network=host --rm volatile_api pytest -v -k test_e2e