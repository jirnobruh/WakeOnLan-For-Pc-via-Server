import socket
import threading
from _datetime import datetime

# Configuration
ServerHost = "0.0.0.0"
ServerPort = 9999
MacAdressPC = ''

def send_wol(mac):
    # Send Wale-On-Lan packet
    try:
        # Create magic packet
        mac_bytes = bytearray.fromhex(mac.replace(':', '').replace('-', ''))
        magic_packet = b'\xff' * 6 + mac_bytes * 16

        # Sending a broadcast packet
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('255.255.255.255', 9))

        print(f"[{datetime.now()}] WoL packet send to MAC: {mac}")
        return True
    except Exception as e:
        print(e)
        return False

def handle_client(client_socket, address):
    # Processing client connections
    try:
        request = client_socket.recv(1024).decode('utf-8').strip()

        if request == 'WAKE_PC':
            print(f"[{datetime.now()}] Received a command from {address[0]}")
            success = send_wol(MacAdressPC)
            response = "SUCCESS" if success else "ERROR"
        else:
            response = "INVALID_COMMAND"

        client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(e)
    finally:
        client_socket.close()

def main():
    # Start server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ServerHost, ServerPort))
    server.listen(5)

    print(f"[{datetime.now()}] WoL server start on port {ServerPort}")
    print(f"[{datetime.now()}] Waiting for commands...")

    while True:
        try:
            client_socket, address = server.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
        except KeyboardInterrupt:
            break

    server.close()

if __name__ == '__main__':
    main()
