# Sample-Peer2Peer
## A single client program to achieve P2P


### System Requirements:
- Python 2.7 should be installed and present in PATH environment variable

Instructions - virtual environment setup:
--> SKIPPED <--

HowTo - testing guidelines:
1) Usability testing needs to be done. It helps focusing on the ease and/or intuitiveness of value extraction.
2) Individual functions should be unit tested (included) once a non-contradictory behaviour has been identified and defined. This is a part of white-box testing.
3) Acceptance testing is needed to ensures that the product meets the acceptability guidelines for integrability in the ecosystem.
4) From a black-box testing perspective, fuzz testing needs to be performed for testing the resiliency.

Instructions - running the unit tests:
1)
2)
3)

Examples - sample run:
1) `./client` <-- this should exit 0, which information around accessing help
2) `./client -h` <-- this should exit 0 with some help information
    2.1) `./client -h` <-- further flags should not be evaluated
3) `./client --help` <-- ditto to point 2. Also prefer "--help" over "-h" as it might be deprecated
    3.1) `./client --help` <-- ditto to point 2.1
4) `./client arg1 -arg2 --arg3` <-- fails due to the incorrectness in argc
5) `./client --arg1 1 --arg2 2 --arg3 3` <-- this should work fine
6) `./client --arg1 1 --arg2 2` <-- ditto as point 5
7) `./client --arg1 1 --arg2 2 --arg3 3,4,5` <-- ditto as point 5
8) `./client --arg1 1, --arg2 --arg3 3,4,` <-- fails as at least one of the argument is malformed
9) `./client --arg4 4 --arg2 2 --arg3 3` <-- fails as an unknown flag encountered
10) `./client --arg1 -1 --arg2 2 --arg3 3,4` <-- fails as at least one of the argument is malformed

Steps - running the application:
1)
2)
3)
4)

