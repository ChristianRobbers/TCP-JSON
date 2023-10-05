from socket import *
import json

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    try:
        operation = int(input("Du kan vælge følgende kommandoer:\n"
                            "Tast 1 og angiv 2 numre for at få et tilfældigt tal imellem dem.\n"
                            "Tast 2 hvis du vil lægge to tal sammen.\n"
                            "Tast 3 hvis du vil trække det ene tal fra det andet.\n"
                            "Tast 4 for at afslutte.\n"
                            "Vælg: "))

        if operation == 4:
            break

        num1 = int(input("Vælg tal 1: "))
        num2 = int(input("Vælg tal 2: "))

        json_data = {
            "operation": "Random" if operation == 1 else ("Add" if operation == 2 else "Subtract"),
            "values": [num1, num2]
        }

        json_string = json.dumps(json_data)
        clientSocket.send(json_string.encode())

        response = clientSocket.recv(1024).decode()
        response_json = json.loads(response)

        if "response" in response_json:
            print('Resultat:', response_json["response"],"\n")
        else:
            print('Invalid response from server:', response)
    except ValueError:
        print("Input skal være et tal / int")

clientSocket.close()