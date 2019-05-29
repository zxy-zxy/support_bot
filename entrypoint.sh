#!/bin/sh

echo "Start application."
export GOOGLE_APPLICATION_CREDENTIALS="$(cat /data/google_credentials.json)"

if [ "$1" = "telegram" ]; then
    python application/manage.py run --platform=telegram
elif [ "$1" = "vk" ]; then
    python application/manage.py run --platform=vk
elif [ "$1" = "init" ]; then
    python application/manage.py init
fi
