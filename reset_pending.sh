#! /bin/bash

cd $(dirname $0)
cd ./.users-pending/
ln -s ../users-enabled/* ./
