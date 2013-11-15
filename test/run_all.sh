#!/bin/bash
pushd test > /dev/null 2>&1

python test_check_datafiles.py
[ $? -ne 0 ] && exit 1

python test_size_to_int.py
[ $? -ne 0 ] && exit 1

popd test > /dev/null 2>&1
