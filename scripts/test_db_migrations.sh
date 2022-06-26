#!/bin/bash
sed -n '2p' ../.env | grep dev;
if [ $? -eq 0 ]
then
    sed '2 s/dev/test/' ../.env | tee ../.env;
else
    sed '2 s/production/test/' ../.env | tee ../.env;
fi
# flask db migrate
# flask db upgrade
echo '[TEST]: Migrations to test DB complete';