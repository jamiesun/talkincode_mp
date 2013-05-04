#!/usr/local/bin/python2.7 
#encoding:utf-8
#
# chkconfig: - 91 35
# description: Starts and stops the talincode server\
# used to provide talincode services.
#
import sys
import os
pid = "/var/run/talincode.pid"
python_exec = '/usr/local/bin/python2.7'
app_dir = "/home/wjt/talkincode"
app_script = "main.py"
def start():
	os.system("cd %s && exec nohup %s %s &"%(app_dir,python_exec,app_script))

def stop():
	os.system("kill %s"%open(pid,'rb').read().strip())
	os.remove(pid)

def restart():
	stop()
	start()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            start()
        elif 'stop' == sys.argv[1]:
            stop()
        elif 'restart' == sys.argv[1]:
            restart()
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)  