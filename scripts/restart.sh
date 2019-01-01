#!/usr/bin/env sh
cd ~/code/knowledgequest
gunicorn -w 3 -b 0.0.0.0:8001 --reload knowledgequest.wsgi:application
sudo service nginx restart
