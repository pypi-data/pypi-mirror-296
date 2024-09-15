#!/bin/bash

echo "IMPORTING ACCOUNT..."
cctt import --password ${PASSWORD} --private-key ${PRIVATE_KEY}

echo "FETCHING BALANCES..."
cctt balances --password ${PASSWORD}

echo "RUNNING..."
cctt run --password ${PASSWORD} ${@}
