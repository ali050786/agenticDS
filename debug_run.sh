#!/bin/bash
echo "Starting debug run" > debug_log.txt
python3 --version >> debug_log.txt 2>&1
python3 collect.py >> debug_log.txt 2>&1
echo "Finished debug run" >> debug_log.txt
