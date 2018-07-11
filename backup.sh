#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source venv/bin/activate
mysqldump  registration_02 > "db_backup/registration_$(date '+%Y-%m-%dT%H:%M:%S')".db
python main.py
deactivate