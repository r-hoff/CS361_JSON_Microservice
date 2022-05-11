import sys
import zmq
from validateJson import validateJson
from expenseReport import createExpenseReport

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # the port that the server will run on
        PORT = sys.argv[1]
    else:
        PORT = 6000

    # set up a socket connection on localhost:PORT
    context = zmq.Context().instance()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://127.0.0.1:{PORT}")

    while True:
        #  Wait for request from client
        request = socket.recv_string()

        # ensure that the request is a valid JSON object and matches expected format
        jsonObj = validateJson(request)
        if not jsonObj:
            errorMsg = "Error: Request is not in valid JSON format"
            socket.send_string(errorMsg)

        else:
            # if valid, create an expense report
            filepath = createExpenseReport(jsonObj)

            # send filepath back to client
            socket.send_string(filepath)

