import zmq
import json
import os

if __name__ == '__main__':

    context = zmq.Context().instance()
    #  Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:6000")

    f = open('example.json')
    jsonObj = json.dumps(json.load(f))

    emptyJson = '{"accounts": [], "transactions": []}'
    badJson = '{"accounts": 1, "balances": []}'

    # send json
    socket.send_string(jsonObj)

    # recv response from server
    response = socket.recv_string()
    print('Response from server: ' + response)

    # open file
    if "No expenses" in response or "Error" in response:
        exit()

    openfile = input("Open file? (y/n): ")
    if openfile == "y":
        os.system(response)
