import sys
import socket
import struct
import select
import random


wined = False


def checker(client_num:int, my_num:int, sign:str) -> str:

    global wined

    if sign.decode() == '=':
        if client_num == my_num:
            wined = True
            return 'Y'
        else:
            return 'K'

    elif sign.decode() ==  '<':
        if client_num > my_num:
            return 'I'
        else:
            return 'N'
    
    elif sign.decode() == '>':
        if client_num < my_num:
            return 'I'
        else:
            return 'N'

def main():

    # Szerver cím és port inicializálása
    server_addr = sys.argv[1]
    server_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server_addr, server_port))

    # Véletlenszám generálása
    random_num = random.randint(1,100)
   # print(f"random szam: {random_num}")

    sock.listen(5)

    packer = struct.Struct("1s i")

    inputs = [sock]
    timeout = 1.0

    while True:
        try:
            readables, _, _ = select.select(inputs, [], [], timeout)

            for s in readables:
                if s is sock:
                    # Új kapcsolatot
                    connection, _ = sock.accept()
                    inputs.append(connection)
                else:
                    # Üzenet fogadása
                    msg = s.recv(packer.size)
                    
                    # Ha nincs üzenet, akkor a kliens lezárta a kapcsolatot
                    if not msg:
                        s.close()
                        inputs.remove(s)
                        continue
                    
                    # Üzenet feldolgozása és válasz küldése
                    (sign,num)  = packer.unpack(msg)
                    print((sign,num))
                    respond = checker(num, random_num, sign)



                    if wined and respond == 'Y':
                        msg = packer.pack(b'Y', 0)
                    elif wined:
                        msg = packer.pack(b'V',0)
                    else:
                        msg = packer.pack(respond.encode(), 0)
                
                        
                    s.sendall(msg)

        except KeyboardInterrupt:
            for s in inputs:
                s.close()
            break

main()