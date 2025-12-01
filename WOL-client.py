import socket
import sys

class WoLClient:
    def __init__(self, server_ip, server_port=9999):
        self.server_ip = server_ip
        self.server_port = server_port

    def send_wake_command(self):
        # Sending a command to turn on the PC
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                sock.connect((self.server_ip, self.server_port))
                sock.send('WAKE_PC'.encode('utf-8'))

                response = sock.recv(1024).decode('utf-8')
                return response == "SUCCESS"

        except Exception as e:
            print(f"Connection error: {e}")
            return False


def main():
    # Replace it with your server's IP address (For example, on the RadminVPN network)
    SERVER_IP = '26.00.00.1'  # Example: IP server in RadminVPN

    client = WoLClient(SERVER_IP)

    print("Sending a command to turn on the PC...")
    if client.send_wake_command():
        print("✅ The command has been sent successfully! The PC should turn on.")
    else:
        print("❌ Error sending the command.")


if __name__ == "__main__":
    main()