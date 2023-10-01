#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ${SCRIPT_DIR}/frontend && docker build -t frontend-image .
cd ${SCRIPT_DIR}/backend && docker build -t backend-image .
cd ${SCRIPT_DIR}/nginx && docker build -t nginx-image .
cd ${SCRIPT_DIR} && docker-compose up

