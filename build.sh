#!/usr/bin/env bash

dirname="$(cd "$(dirname "$0")"; pwd)"

cd $dirname/vuefront
npm run build
#cp -r "${dirname}/vuefront/dist/" "${dirname}/server/static/"
