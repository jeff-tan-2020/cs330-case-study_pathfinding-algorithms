#!/bin/bash
echo "script started"

for n in {1..10}; do python "t4.py"; done #for single CPU

echo "script completed"