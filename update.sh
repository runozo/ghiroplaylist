#!/usr/bin/env bash
source ./env/bin/activate
python get_my_playlist.py
git commit -am "`date`"
git push origin master