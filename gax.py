import os
import sys

def byte_add(*args):
    ans = 0
    for i in args:
        ans += i
    return ans & 0xff

class ANIM():
    def switch_key(key: bytearray, ch: int):
        t = ch
        ch &= 7
        if ch == 0:
            key[0] = byte_add(key[0], t)
            key[3] = byte_add(key[3], t, 2)
            key[4] = byte_add(key[2], t, 11)
            key[8] = byte_add(key[6]+7)
        elif ch == 1:
            key[2] = byte_add(key[9], key[10])
            key[6] = byte_add(key[7], key[15])
            key[8] = byte_add(key[8], key[1])
            key[15] = byte_add(key[5], key[3])
        elif ch == 2:
            key[1] = byte_add(key[1], key[2])
            key[5] = byte_add(key[5], key[6])
            key[7] = byte_add(key[7], key[8])
            key[10] = byte_add(key[10], key[11])
        elif ch == 3:
            key[9] = byte_add(key[2], key[1])
            key[11] = byte_add(key[6], key[5])
            key[12] = byte_add(key[8], key[7])
            key[13] = byte_add(key[11], key[10])
        elif ch == 4:
            key[0] = byte_add(key[1], 111)
            key[3] = byte_add(key[4], 71)
            key[4] = byte_add(key[5], 17)
            key[14] = byte_add(key[15], 64)
        elif ch == 5:
            key[2] = byte_add(key[2], key[10])
            key[4] = byte_add(key[5], key[12])
            key[6] = byte_add(key[8], key[14])
            key[8] = byte_add(key[11], key[0])
        elif ch == 6:
            key[9] = byte_add(key[11], key[1])
            key[11] = byte_add(key[13], key[3])
            key[13] = byte_add(key[15], key[5])
            key[15] = byte_add(key[9], key[7])
            key[1] = byte_add(key[9], key[5])
            key[2] = byte_add(key[10], key[6])
            key[3] = byte_add(key[11], key[7])
            key[4] = byte_add(key[12], key[8])
        elif ch == 7:
            key[1] = byte_add(key[9], key[5])
            key[2] = byte_add(key[10], key[6])
            key[3] = byte_add(key[11], key[7])
            key[4] = byte_add(key[12], key[8])
        return key

    def decrypt(data: bytes):
        key = bytearray(data[4:20])
        data = bytearray(data[20:])
        length = len(data)
        v = 0
        for i in range(length):
            data[i] = key[v] ^ data[i]
            v += 1
            if v == 16:
                v = 0
                key = ANIM.switch_key(key, data[i-1])
        return data


    def encrypt(data: bytes):
        length = len(data)
        key = bytearray(b'\x00'*16)
        new_data = b'\x00\x00\x00\x01'+key+b'\x00'*length
        new_data = bytearray(new_data)

        v = 0
        for i in range(length):
            new_data[20+i] = key[v] ^ data[i]
            v += 1
            if v == 16:
                v = 0
                key = ANIM.switch_key(key, data[i-1])
        return new_data


if len(sys.argv) != 4:
    print("Usage: gax.py <-d|-i> <input_file> <output_file>")
    print(" -d: dump .gax to .png")
    print(" -i: convert .png to .gax")
    sys.exit(1)

mode = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]


if mode == '-i':
    with open(input_file, 'rb') as f:
        input_data = f.read()

    output_data = ANIM.encrypt(input_data)

elif mode == '-d':
    with open(input_file, 'rb') as f:
        input_data = f.read()

    output_data = ANIM.decrypt(input_data)

else:
    print("Usage: gax.py <-d|-i> <input_file> <output_file>")
    print(" -d: dump .gax to .png")
    print(" -i: convert .png to .gax")
    sys.exit(1)

with open(output_file, 'wb') as f:
    f.write(output_data)
    print("Success!")
