# Server Configuration Wake-on-LAN

# Server Parameters
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

# MAC address of the target computer to wake up
TARGET_MAC = 'FF-FF-FF-FF-FF-FF'                # <-- change MAC address PC

# List of broadcast IP addresses for different networks
BROADCAST_IPS = [
    '192.168.0.15',                             # <-- change to the IP address of the computer you want to turn on
    '255.255.255.255'
]

# Параметры для локальной сети
LOCAL_NETWORK = {
    'broadcast_ip': '192.168.0.255', # Broadcast address for network /24
    'source_interface_ip': '192.168.0.16'       # <-- change to the server's IP address in local network
}