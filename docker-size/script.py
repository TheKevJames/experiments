from Crypto.Hash import SHA256


INPUT = 'message'.encode('utf-8')
OUTPUT = (b'\xabS\n\x13\xe4Y\x14\x98+y\xf9\xb7\xe3\xfb\xa9\x94\xcf\xd1\xf3'
          b'\xfb"\xf7\x1c\xea\x1a\xfb\xf0+F\x0cm\x1d')


if __name__ == '__main__':
    hash = SHA256.new()
    hash.update(INPUT)
    print(hash.digest() == OUTPUT)
