#!/usr/bin/env ruby
begin
    until 1 == 2 do
        print 'Enter a word: '
        $stdout.flush
        word = gets

        puts word.length % 2 == 0 ? '*' * (word.length - 1) : word
    end
rescue Exception => e
    puts ''
end
