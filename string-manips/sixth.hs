import System.IO

main :: IO()
main = do
    putStr "Enter a word: "
    hFlush stdout
    word <- getLine
    print (count word)
    main

cons :: Char -> Bool
cons x = elem x "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

count :: [Char] -> Integer
count [] = 0
count (x:xs)
    | cons x = 1 + count xs
    | otherwise = 0 + count xs
