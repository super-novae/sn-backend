#!/bin/bash
sed -n '2p' ../.env | grep test;
if [ $? -eq 0 ]
then
    sed '2 s/test/dev/' ../.env | tee ../.env;
else
    sed '2 s/production/dev/' ../.env | tee ../.env;
fi
# flask db migrate
# flask db upgrade
echo -e '\n[DEV]: Migrations to dev DB complete';