#!/usr/bin/env racket
#lang racket

(define (swap word)
    (display (regexp-replace* "([aeiou])(.*?)([aeiou])" word "\\3\\2\\1"))
    (newline))

(define (main)
    (printf "Enter a word: ")
    (let ([command (read-line (current-input-port) 'any)])
        (swap command)
        (main)))

(main)
