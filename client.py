import sys
import socket
import struct
import random
import time


def main():   
    server_addr = sys.argv[1]
    server_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_addr, server_port))

    packer = struct.Struct("1s i")

    low = 1
    high= 99
    guessed_number = (low + high) // 2
    actual_sign = b'>' 


    while True:
        #print(f'{low} - {high}')

        rand_time = random.randint(1,6)
        time.sleep(rand_time)
        
        if low >= high:
            actual_sign = b'=' 
            guessed_number = high  # Az egyetlen lehetséges szám
            sock.sendall(packer.pack(actual_sign, guessed_number))
        elif low  == high - 1:
            actual_sign = b'>'
            guessed_number = low
            sock.sendall(packer.pack(actual_sign, guessed_number))
        else:
            sock.sendall(packer.pack(actual_sign, guessed_number))
        
        # Válasz a szervertől
        msg = sock.recv(packer.size)
        server_response, _ = packer.unpack(msg)

        if server_response.decode() == 'Y':
                    mesage_tupple = ('Y',0)
                    print(mesage_tupple)
                    break
        elif server_response.decode() == 'V':
                    mesage_tupple = ('V',0)
                    print(mesage_tupple)
                    break
        elif server_response.decode() == 'K':
                    mesage_tupple = ('K',0)
                    print(mesage_tupple)
                    break

        if server_response.decode() == 'I':
                low = guessed_number + 1
                guessed_number = (low + high) // 2
        elif server_response.decode() == 'N':
                high = guessed_number
                guessed_number = (low + high) // 2

main()