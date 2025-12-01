# Launch your PC via WakeOnLan using an additional server
## Requirements
```
python 3.9+ on Server and Client
Enabled WakeOnLan on the PC to be enabled
```
## How it work
In the client (for example, on a laptop), you run WOL-client.py he sends a request to the server, which sends a magic packet to the computer that needs to be turned on.
## How to enable WakeOnLan in PC
Instruction for [Asus](https://www.asus.com/support/faq/1045950/) 

Instruction for [MSI](https://www.msi.com/support/technical_details/MB_Wake_On_LAN)
## Installation
1) Download zip arhive or use 
```
git clone https://github.com/jirnobruh/WakeOnLan-For-Pc-via-Server.git
```
2) On Server:
   in server_config.py change TARGET_MAC, in BROADCAST_IPS local IP to computer you want to turn on and in LOCAL_NETWORK change to the server's IP address in local network
3) On Client:
   in client_config.py change SERVER_IP and SERVER_PORT to the corresponding SERVER_HOST and SERVER_PORT specified in server_config.py
4) Start WOL-for-server.py or start_server.bat (If you configure it inside the file) in Server
5) If you need to start the PC via Wake On Lan, then run on the client WOL-client.py or start_pc.bat (If you configure it inside the file)
## How I use this
I don't have a white IP address, and I use RadminVPN to make a local network between the client and the server. In theory, this should work smoothly on white IP addresses.
