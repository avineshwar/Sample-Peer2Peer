# Sample-Peer2Peer
## A single client program to achieve P2P


### System Requirements:
- Python 2.7 should be installed and present in PATH environment variable

### Instructions - virtual environment setup:
--> SKIPPED <--

### HowTo - testing guidelines:
- Usability testing is pending.
-- It helps focusing on the ease and/or intuitiveness of value extraction.
- Individual functions should be unit tested (tests not included) once a non-contradictory behaviour has been identified and defined.
-- This is a part of white-box testing.
- Acceptance testing is needed to ensures that the product meets the acceptability guidelines for integrability in the ecosystem.
- From a black-box testing perspective, fuzz testing needs to be performed for testing the resiliency.

### Instructions - running the unit tests:
--> SKIPPED <--

### Steps - running the application (this is described in "Graph" below):
- `./client.py --name A --port 8001 &`
- `./client.py --name B --port 8002 &`
- `./client.py --name C --port 8003 --bootnodes A:8001,B:8002 &`

### Sample - Test run:
- `curl localhost:8001`
- `curl localhost:8002`
- `curl localhost:8003`
- `curl localhost:8003/whisper?name=foo&message=hello`
- `curl localhost:8003/whisper?name=bar&message=hello`
- `curl localhost:8002/whisper?name=baz&message=hello`
- `curl localhost:8001/whisper?name=baz&message=hello`


### Graph - Connection map:
```
Foo
 ^
 |      Bar
 |       ^
 |       |
Baz------|
```

### Design Ideology - How is it designed:
- The listening code (server) runs in a thread separate from the main thread.
- The program (main thread) will not exit till the listening code (a separate thread) is running.
- For a client to connect to another client, two out of one way has to possible:
- The connection request itself specify the necessary information to connect, OR,
- The client is already having the necessary information to connect; otherwise a _Request cannot be fulfilled_ message is appropriate.
- This is a design limitation which can be overcome by having a reference information present on the system to which all the clients agree to contribute to. In a distributed environment, such a system might not exist at all (or locally).

_Print statements at proper locations can give an insight of the state machine, at any given time. They have been removed._

### Improvements:
- Non-blocking calls can be leveraged.
- An explicit clean-up function can be called for interrupted runs or even in case of an exception for deeper (and procedural) roll-back/clean-up.
- Unit tests can be written first to which the design should then conform.
