#!/bin/sh
while
    true
do
    /usr/local/bin/python /home/tester/tools/python/python_project/sbu_pdt/version_get.py > /dev/null 2>&1
    sleep 60
done
