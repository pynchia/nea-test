# TCP Client/Server Test

Build a tcp client and a tcp server with python > 3.5.x.

The server should listen on port 3443.

The server should accept a maximum of 100 connected clients.

The server should send the current date to each client every 10 seconds.

The client should be a command line application and should connect to the server with a TLS connection.

Once started the client should receive the current date from the server every 10 seconds.

The client should listen to the standard input and send a text message to the server every time the return key is pressed, the server should respond to the client with the same string but reversed.

All the implementation must be covered  with automated tests.

## Setup

Clone the repository:

`git clone git@github.com:pynchia/nea-test.git`

Descend into the newly created directory:

`cd nea-test/`

Create the virtual environment:

`python3 -m venv .venv`

Activate the virtual environment:

`. .venv/bin/activate`

Upgrade pip:

`pip install -U pip`

Install the requirements:

the external packages first
`pip install -r requirements.txt`

and then the internal modules
`pip install .`

## Execute the tests

`. ./run-tests.sh`

## Launch the server

`servercli`

## Launch the client(s)

For each client:

- open a new terminal
- descend into the same project directory (`nea-test/`)
- activate the virtual environment (`. .venv/bin/activate`)
- launch the client with `clientcli`

## Notes and Improvements

### In-band messaging

The server response (the reversed string) and the date are sent on the same channel to the client (i.e. in-band signalling in telecoms parliance).
In order to be able to tell them apart and interpret the contents in a cleaner way, we could send such payloads as part of a structured message, e.g. serialised in JSON format:

{
    "msg_type": "string" or "date",
    "payload": either the reversed string or the date
}

To such aim, the `nea.services.message` module contains a class to encode/decode such message structure and the code already contains a few references to it (now commentated out)

### Date-broadcaster optimisation

The server date broadcaster is active even if there are no clients connected.

It sleeps for ten seconds then it sends the date to all the clients.

The cpu time spent checking the list of clients is negligible, but from a purist point of view it could be avoided.

Simply put, the broadcaster task could be cancelled when the only remaining client disconnects and be created when the first client connects.
