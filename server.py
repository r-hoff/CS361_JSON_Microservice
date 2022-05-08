import zmq
from validateJson import validateJson
from expenseReport import createExpenseReport

# the port that the server will run on
PORT = 6000

# set up a socket connection on localhost:PORT
context = zmq.Context().instance()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://127.0.0.1:{PORT}")

while True:
    #  Wait for request from client
    request = socket.recv_string()
    print('Request from client: ' + request)

    # ensure that the request is a valid JSON object and matches expected format
    jsonObj = validateJson(request)
    if not jsonObj:
        errorMsg = "Error: Request is not in valid JSON format"
        socket.send_string(errorMsg)
        print('Response to client: ' + errorMsg)
    else:
        # if valid, create an expense report
        filepath = createExpenseReport(jsonObj)

        # send filepath back to client
        socket.send_string(filepath)
        print('Response to client: ' + filepath)
