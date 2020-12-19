#!/bin/bash

cd /srv/imgcity

source venv/bin/activate

python3.6 -m app.server app.yaml
