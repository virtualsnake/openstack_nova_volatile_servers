#!/usr/bin/env bash

docker run -p5000:5000 --env-file openstack.env --rm volatile_api