#!/bin/bash -x

source .env

# handle all non-zero exit status codes with a slack notification
trap 'handler $? $LINENO' ERR

handler () {
    printf "%b" "${FAIL} ✗ ${NC} dist build failed on line $2 with exit status $1\n"
}

printf "%b" "${OKB}Building package distribution${NC}"
python setup.py sdist bdist_wheel
printf "%b" "${OKG} ✓ ${NC}complete\n"