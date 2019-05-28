#!/bin/sh

echo "Start application."
export GOOGLE_APPLICATION_CREDENTIALS="$(cat /data/google_credentials.json)"


if [ "$1" = "telegram" ]; then
    python manage.py run --platform=telegram
elif [ "$1" = "vk" ]; then
    python manage.py run --platform=vk
elif [ "$1" = "init" ]; then
    python manage.py init
fi
