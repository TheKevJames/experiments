#!/usr/bin/env bash
rm -f results.txt
echo "Aggregate Results over ${NUM_TESTS} runs" > results.txt
echo >> results.txt

echo "Log Handler" >> results.txt
python bin/log.py 2>/dev/null >> results.txt
echo >> results.txt

echo "Log Handler with Sentry" >> results.txt
python bin/log-plus-sentry.py 2>/dev/null >> results.txt
echo >> results.txt

echo "Exception Handler" >> results.txt
python bin/except.py 2>/dev/null >> results.txt
echo >> results.txt

echo "Exception Handler with Sentry" >> results.txt
python bin/except-plus-sentry.py 2>/dev/null >> results.txt


cat results.txt
