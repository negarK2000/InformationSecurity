import socket

HOST = '127.0.0.1'
PORT = 5000
length = 1024


def handle_request(conn):
    conn.send('connected.'.encode())

    print("Enter system info for client system information:")
    i = input()

    while i != 'sysinfo':
        print("invalid command !\nenter system info for client system information:")
        i = input()

    if i == 'sysinfo':
        conn.send('send the data...'.encode())
        data = conn.recv(2*length).decode('utf-8')

        temp = data.split(',')
        for item in temp:
            print(item)

        if not data:
            return

    print("enter x to close the connection:")
    return input()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket is successfully created.")

    s.bind((HOST, PORT))
    s.listen(5)
    print("Socket is listening...")

    connection, info = s.accept()
    print(f'"host:{info[0]}, port:{info[1]}" connected.')

    while True:
        o = handle_request(connection)

        if o == 'x':
            connection.send('end'.encode())
            connection.send('connection is closed.'.encode())
            break
        else:
            connection.send('continue'.encode())

    s.close()
