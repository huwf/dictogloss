#!/usr/bin/env bash

# Write the config file
secret_key=$(hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/urandom)
salt=$(hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/urandom)

if [ ! -f ./config.py ]; then

    cat << EOF > ./config.py
SECRET_KEY = '${secret_key}'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = '${salt}'
# SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
EOF
fi

docker-compose pull
docker-compose up -d
