#!/bin/bash
echo "Starting Pool Monitor Add-on"
POOL_LITERS=$(jq --raw-output '.pool_liters' /data/options.json)
POOL_TYPE=$(jq --raw-output '.pool_type' /data/options.json)
echo "Pool Liters: $POOL_LITERS"
echo "Pool Type: $POOL_TYPE"
