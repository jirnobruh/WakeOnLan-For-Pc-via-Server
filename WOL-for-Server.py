import socket
import threading
from server_config import (
    SERVER_HOST,
    SERVER_PORT,
    TARGET_MAC,
    BROADCAST_IPS,
    LOCAL_NETWORK
)

class WoLServer:
    def __init__(self):
        self.host = SERVER_HOST
        self.port = SERVER_PORT
        self.target_mac = TARGET_MAC
        self.broadcast_ips = BROADCAST_IPS
        self.local_network = LOCAL_NETWORK

    def create_magic_packet(self, mac):
        """Creates magic packet for Wake-on-LAN"""
        # Remove separators from MAC address
        mac_clean = mac.replace(':', '').replace('-', '')

        # Check MAC address length
        if len(mac_clean) != 12:
            raise ValueError(f"Invalid MAC address length: {mac}")

        # Convert MAC to bytes
        mac_bytes = bytes.fromhex(mac_clean)

        # Create magic packet: 6xFF + 16*MAC
        return b'\xff' * 6 + mac_bytes * 16

    def wake_up_pc_specific_network(self):
        """Sends WoL via local network 192.168.0.x"""
        success = False

        print(f"Attempting to send WoL via local network...")
        print(f"Broadcast IP: {self.local_network['broadcast_ip']}")
        print(f"Source interface IP: {self.local_network['source_interface_ip']}")

        # Send via the local network
        success = self.send_wol_via_interface(
            self.local_network['broadcast_ip'],
            self.local_network['source_interface_ip']
        )

        return success

    def send_wol_via_interface(self, target_ip, interface_ip=None):
        """Sends WoL packet through specified interface"""
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            # If the interface IP is specified, we bind the socket to it.
            if interface_ip:
                sock.bind((interface_ip, 0))
                print(f"Socket bound to interface: {interface_ip}")

            # Create magic packet
            magic_packet = self.create_magic_packet(self.target_mac)

            # Send it to the broadcast address
            sock.sendto(magic_packet, (target_ip, 9))
            print(f"✅ Magic packet sent to {self.target_mac} via broadcast {target_ip}")
            if interface_ip:
                print(f"   Using source interface: {interface_ip}")

            sock.close()
            return True

        except Exception as e:
            print(f"❌ Error sending WoL packet: {e}")
            return False

    def handle_client(self, conn, addr):
        """Handles client connection"""
        print(f"Connection from {addr}")

        try:
            data = conn.recv(1024).decode('utf-8').strip()

            if data == 'WAKE_PC':
                print("Wake command received")
                if self.wake_up_pc_specific_network():
                    conn.send("SUCCESS".encode('utf-8'))
                else:
                    conn.send("ERROR".encode('utf-8'))
            else:
                print(f"Unknown command: {data}")
                conn.send("UNKNOWN_COMMAND".encode('utf-8'))

        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            conn.send("ERROR".encode('utf-8'))
        finally:
            conn.close()

    def start_server(self):
        """Starts the server"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"WoL Server listening on {self.host}:{self.port}")
            print(f"Target MAC: {self.target_mac}")
            print("Broadcast IPs:")
            for ip in self.broadcast_ips:
                print(f"  - {ip}")

            while True:
                conn, addr = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()

def main():
    server = WoLServer()

    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")


if __name__ == "__main__":
    main()