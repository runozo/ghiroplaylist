#!/usr/bin/env bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
USER="xxx"
PASSWORD="xxx"
PHONE_ID="xxx"
python get_my_playlist.py $USER $PASSWORD $PHONE_ID
git commit -am "`date`"
git push origin master