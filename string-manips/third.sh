#!/bin/bash
while true; do
    read -p "Enter a word: " word
    num=${#word}
    echo ${word:num/2}${word:0:num/2}
done;
