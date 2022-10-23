#! /bin/bash

"""
Usage: [TEST_PATH=<path>] ./test-parser-stage.sh

    TEST_PATH: path to minidecaf-tests
"""

default_path="./minidecaf-tests"
testpath=${TEST_PATH:-$default_path}

test_parse() {
    for step in {1..6}; do
        for filepath in $testpath/testcases/step$step/*.c; do

            if [ ! -e $filepath ]; then
                echo "Wrong TEST_PATH. Please set it to the path to minidecaf-tests."
                exit
            fi

            filename=${filepath##*/}
            errpath=./errors/step$step
            errfile=$errpath/${filename%.*}.log

            [ ! -d $errpath ] && mkdir -p $errpath

            if ! python main.py --input $filepath --parse > /dev/null 2> $errfile; then
                echo "parser test failed for $filepath"
                echo "error message saved in $errfile"
                echo
            fi
        done
    done
}

test_parse
