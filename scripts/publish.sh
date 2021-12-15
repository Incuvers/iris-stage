#!/bin/bash
source .env

SERVICE=""
USERNAME=""
PASSWORD=""
REPO_URL=""

while getopts ":hs:r:u:p:" opt; do
    case "$opt" in
        h )
            echo "Usage:"
            echo "      publish.sh -h                                                           Display this message"
            echo "      publish.sh -s pypi -r "$REPOSITORY_URL" -p "$PASSWORD" -u $USERNAME     Publish dist to pypi"
            exit 0;
            ;;
        s )
            SERVICE="$OPTARG"
            ;;
        r )
            REPO_URL="$OPTARG"
            ;;
        p )
            PASSWORD="$OPTARG"
            ;;
        u )
            USERNAME="$OPTARG"
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            exit 1;
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            exit 1;
            ;;
    esac
done

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$REPO_URL" ] || [ -z "$SERVICE" ]; then
    printf "%b" "${FAIL}Missing arguments${NC}\n"
    exit 1
fi

printf "%b" "${OKB}Uploading package distribution${NC}\n"
python3 -m twine upload -r "$SERVICE" -u "$USERNAME" -p "$PASSWORD" --repository-url "$REPO_URL" dist/* --verbose
printf "%b" "${OKG} ✓ ${NC}complete\n"