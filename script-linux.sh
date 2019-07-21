#!/bin/sh

./cloud_sql_proxy -instances="cs-348:us-east1:perfectparty"=tcp:3306 -credential_file=credential.json
