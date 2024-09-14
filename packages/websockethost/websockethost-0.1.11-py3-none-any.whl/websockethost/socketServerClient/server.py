import socket
from websockethost.socketServerClient.ThreadScripts.ThreadForClient import ThreadForClient

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_socket_server(host: str, port: int, log_file: str, init_data: bool):
	adress = (host, port)
	server.bind(adress)	
	while True:
		try:
			server.listen(5)
			client, addr = server.accept()
				
			with open(log_file, "a+") as logs:
				logs.write(f"The connection as create on : {addr}")

			my_thread = ThreadForClient(client, add_table=init_data)
			my_thread.start()
			
		except KeyboardInterrupt:
			break

	client.close()
	server.close()
