import os
import pyaes
import pbkdf2
import binascii
import secrets
import sys


def read_file(f_name, mode):
    file = open("./files/" + f_name, mode)
    txt = file.readlines()
    file.close()
    return txt


def write_file(f_name, cont, mode):
    file = open("./files/" + f_name, mode)
    file.writelines(cont)
    file.close()


def get_key():
    key = read_file('init_key.txt', 'rb')[0]

    salt = os.urandom(32)
    new_key = pbkdf2.PBKDF2(key, salt).read(32)

    print('AES encryption key:', binascii.hexlify(new_key, '-'))

    print(new_key)
    write_file('key.txt', [new_key], 'wb')

    return new_key


def encrypt():
    res = []
    key = get_key()

    plaintext = read_file('plaintext.txt', 'r')
    print('plaintext: ', plaintext)

    iv = secrets.randbits(256)

    for item in plaintext:
        counter = pyaes.Counter(initial_value=iv)
        aes = pyaes.AESModeOfOperationCTR(key, counter=counter)
        ciphertext = aes.encrypt(item)

        print('ciphertext: ', ciphertext)
        res.append(ciphertext)

    write_file('ciphertext.txt', res, 'wb')
    write_file('initial_vector.txt', [str(iv)], 'w')


def decrypt():
    res = []
    key = read_file('key.txt', 'rb')[0]

    ciphertext = read_file('ciphertext.txt', 'rb')
    print('ciphertext: ', ciphertext)

    iv = int(read_file('initial_vector.txt', 'r')[0])

    for item in ciphertext:
        counter = pyaes.Counter(initial_value=iv)
        aes = pyaes.AESModeOfOperationCTR(key, counter=counter)
        deciphertext = aes.decrypt(item)

        deciphertext = deciphertext.decode("utf-8")
        print('decipher text: ', deciphertext)
        res.append(deciphertext)

    write_file('deciphertext.txt', res, 'w')


def do_both():
    res = []
    key = get_key()

    plaintext = read_file('plaintext.txt', 'r')
    print('plaintext: ', plaintext)

    iv = secrets.randbits(256)

    for item in plaintext:
        counter = pyaes.Counter(initial_value=iv)
        aes = pyaes.AESModeOfOperationCTR(key, counter=counter)
        ciphertext = aes.encrypt(item)

        print('ciphertext: ', ciphertext)
        res.append(ciphertext)

    for item in res:
        counter = pyaes.Counter(initial_value=iv)
        aes = pyaes.AESModeOfOperationCTR(key, counter=counter)
        deciphertext = aes.decrypt(item)

        deciphertext = deciphertext.decode("utf-8")
        print('decipher text: ', deciphertext)


def main():
    arg = sys.argv[1].lower()

    if arg == 'e':
        encrypt()
    elif arg == 'd':
        decrypt()
    elif arg == 'b':
        do_both()


if __name__ == '__main__':
    main()
