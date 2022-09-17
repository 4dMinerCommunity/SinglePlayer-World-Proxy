import sys


if sys.argv[1] == "client":
    from client import  run_client
    run_client()
elif sys.argv[1] == "server":
    from src import runserver
    runserver()
    