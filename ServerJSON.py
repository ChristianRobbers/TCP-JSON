from socket import *
import threading
import json
import random

def handle_client(connectionSocket, addr):
    print(addr[0])
    keep_communicating = True

    while keep_communicating:
        try:
            data = connectionSocket.recv(1024).decode()
            if not data:
                break

            json_data = json.loads(data) # Dezerialisere JSON data fra client
            
            if "operation" in json_data and "values" in json_data:
                operation = json_data["operation"]
                values = json_data["values"]

                if operation == "Random":
                    if len(values) == 2 and values[0] <= values[1]:
                        responseClient = random.randint(values[0], values[1])
                    else:
                        responseClient = "Fejl: Det første tal kan ikke være større end det andet tal"
                elif operation == "Add":
                        responseClient = sum(values)
                elif operation == "Subtract":
                        responseClient = values[0] - values[1]
            else:
                responseClient = "Fejl: Forkert JSON format"

            response_json = json.dumps({"response": responseClient})
            connectionSocket.send((response_json + "\r\n").encode())

        except ValueError:
            connectionSocket.send("Fejl: Forkert JSON format\r\n".encode())

    connectionSocket.close()

serverName = "localhost"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('Server is ready to listen')
while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()