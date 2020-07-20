# Client/Server Test

Build a tcp client and a tcp server with python > 3.5.x.

The server should listen on port 3443.

The server should accept a maximum of 100 connected clients.

The server should send the current date to each client every 10 seconds.

The client should be a command line application and should connect to the server with a TLS connection.

Once started the client should receive the current date from the server every 10 seconds.

The client should listen to the standard input and send a text message to the server every time the return key is pressed, the server should respond to the client with the same string but reversed.

All the implementation must be covered  with automated tests.

## Setup and execution of the tests

`docker build --no-cache --target pybuild -t testbuild .`

`docker run -it testbuild`

## Setup and execution of the server

Go to the root `nea-test` directory and build the docker image

`docker build -t appbuild .`

Launch it

`docker run -it -p 3443:3443 appbuild servercli`

## Setup and execution of the clients

For each client, open a new terminal and launch the client

`docker run -it 
-p 3443:3443
appbuild clientcli`

## Notes and Improvements

The server response (the reversed string) and the date are sent on the same level to the client (i.e. in-band signalling in telecoms parliance).
In order to be able to tell them apart and interpret the contents in a cleaner way, we could send such payloads as part of a structured message, e.g. serialised in JSON format:

{
    "msg_type": "string" or "date",
    "payload": either the reversed string or the date
}

To such aim, the `nea.services.message` module contains a class to encode/decode such message structure.
