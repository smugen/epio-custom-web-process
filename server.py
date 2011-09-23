from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_unix_socket
import tornado.process as process
from tornado.ioloop import IOLoop
from app import app
import os
import sys
import signal

def task_id(tid):
    return "#%s" % tid if tid != None else "MAIN"

def sigterm_handler(signum, frame):
    print >> sys.stderr, "%s: SIGTERM received. Exiting..." % \
                         task_id(process.task_id())
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    sockets = [bind_unix_socket(sys.argv[1] if len(sys.argv)>1 else None)]

    if "fork" in os.__dict__:
        print "%s: %s cpu(s) detected, spawning..." % \
              (task_id(process.task_id()), process.cpu_count())
        child_id = task_id(process.fork_processes(0))
        if child_id != "MAIN":
            print "%s: listen on %s" % (child_id, sockets)
        else:
            print "%s: All child processes have exited normally. Exiting..." % \
                  child_id
            sys.exit(0)
    else: print "forking not available, use single-process."

    http_server = HTTPServer(WSGIContainer(app))
    http_server.add_sockets(sockets)
    IOLoop.instance().start()
