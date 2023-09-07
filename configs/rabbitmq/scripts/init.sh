#!/bin/bash
# This script is executed inside the container.

set -e

# check command exists
function exit_if_command_not_exists() {
    exit_if_empty "$1"

    if ! command -v "$1" >/dev/null 2>&1; then
        echo "ERROR: command does not exist $1"
        exit 1
    fi
}

# replace string in the file
function replace() {
    exit_if_empty "$1"
    exit_if_empty "$2"
    exit_if_empty "$3"

    sed -i "s|$1|$2|g" "$3"
}

function encode_password() {
    exit_if_empty "$1"

    SALT=$(od -A n -t x -N 4 /dev/urandom)
    PASS=$SALT$(echo -n $1 | xxd -p | tr -d '\n' | tr -d ' ')
    PASS=$(echo -n "$PASS" | xxd -r -p | sha256sum | head -c 128)
    PASS=$(echo -n "$SALT$PASS" | xxd -r -p | base64 | tr -d '\n')
    echo "$PASS"
}

# exit if env variable is empty
function exit_if_empty() {
    if [[ -z "$1" ]]; then
        echo "ERROR: env variable does not set"
        exit 1
    fi
}

# templates to replace
ADMIN_PASS_TEMPLATE="<admin_hashed_password>"
GUEST_PASS_TEMPLATE="<guest_hashed_password>"

# file to replace
FILE="/etc/rabbitmq/definitions.json"

#check env variables
ENV_VARIABLES=(
    RABBITMQ_ADMIN_PASSWORD
    RABBITMQ_GUEST_PASSWORD
    RABBITMQ_ADMIN_USER
    RABBITMQ_GUEST_USER
)
for item in "${ENV_VARIABLES[@]}"; do
    exit_if_empty "${!item}"
done

# check if file exists
if [[ ! -f "$FILE" ]]; then
    echo "ERROR: file does not exist $FILE"
    exit 1
fi

# check commands exist
COMMANDS=(
    od
    base64
    sed
    sha256sum
    xxd
    base64
    tr
    head
)
for item in "${COMMANDS[@]}"; do
    exit_if_command_not_exists "$item"
done

# generate password's hashes
ADMIN_PASS=$(encode_password "$RABBITMQ_ADMIN_PASSWORD")
GUEST_PASS=$(encode_password "$RABBITMQ_GUEST_PASSWORD")

# replace passwords in definitions.json
replace $ADMIN_PASS_TEMPLATE "$ADMIN_PASS" "$FILE"
replace $GUEST_PASS_TEMPLATE "$GUEST_PASS" "$FILE"

exit 0
