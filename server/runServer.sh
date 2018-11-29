#!/bin/bash

> cloudletStore.json
python3 server.py '128.237.129.242' '80' &
python3 tinyClient.py '128.237.129.242' '72' 'P' &

