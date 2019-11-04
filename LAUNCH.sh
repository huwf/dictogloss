#!/usr/bin/env bash

# Write the config file
secret_key=$(hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/urandom)
salt=$(hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/urandom)
echo "Enter the email for the default account"
read email
echo "Enter the password for the default account"
read -s password

if [ ! -f ./config.py ]; then

    cat << EOF > ./config.py

config = {
    'SECRET_KEY': '${secret_key}',
    'SECURITY_PASSWORD_HASH': 'pbkdf2_sha512',
    'SECURITY_PASSWORD_SALT': '${salt}',
    '# SECURITY_USER_IDENTITY_ATTRIBUTES': 'username',
}
EOF
fi
cat << EOF > ./.env
EMAIL=${email}
PASSWORD=${password}
EOF
#docker-compose pull
#docker-compose up -d
