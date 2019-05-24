#!/bin/sh

echo "Start application."
export GOOGLE_APPLICATION_CREDENTIALS="$(cat data/google_credentials.json)"
python manage.py run --platform=vk