#! /bin/bash

project_path=$(cd `dirname $0`; pwd)
cd ./.users-pending/
ln -s ../users-enabled/* ./
