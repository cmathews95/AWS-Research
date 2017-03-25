#Run with Python 2.6
import os
import sys
import socket
import threading
import MySQLdb
import random

#Get Unique Instance ID
ID = MySQLdb.escape_string(str(os.popen("ec2-metadata -i").read()).strip('\n').strip('instance-id:').strip(' '))
print  ID

#Connect to db
db = MySQLdb.connect(
         host="metricstestdb.cw4l1lykzmxj.us-west-1.rds.amazonaws.com",
         port=3306,
         user="cs199admin",
         passwd="cs199password",
         db="metrics_test_db")
cur = db.cursor()
add_message = ("INSERT INTO messages "
               "(instanceID, message) "
               "VALUES (%s, %s)")

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def saveData(name, connection):
    # Receive the data in small chunks and retransmit it
    data = MySQLdb.escape_string(connection.recv(200))
    # f = open("metrics-log.txt","w+")
    # f.write(data)
    # f.write('\n')
    # f.close()
    print >>sys.stderr, 'received "%s"' % data
    data_message = (ID, data)
    cur.execute(add_message, data_message)
    db.commit()
    connection.sendall("Added: " + data)
    connection.close()

#AWS Load Balancer Health Check Listener
def healthCheck():
    #Create a tcp/ip socket to accept load balancer health checks
    lb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_address = (get_ip_address(), 4000)
    lb_sock.bind(lb_address)
    lb_sock.listen(5)
    while True:
        h_connection, h_client_address = lb_sock.accept()
        h_connection.sendall("Confirm")
        h_connection.close()

def Main():
    #lb_thread = threading.Thread(target=healthCheck, args=("thread"))
    #lb_thread.start()

    #Create a tcp/ip socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (get_ip_address(), 8000)
    print >> sys.stderr, 'Starting server on %s port %s' % server_address

    try:
        # Listen for incoming connections
        sock.bind(server_address)
        sock.listen(6)
        while True:
            # Wait for a connection
            connection, client_address = sock.accept()
            print "Client connected ip: <" + str(client_address) + ">"
            t = threading.Thread(target=saveData, args=("thread", connection))
            t.start()
    except (KeyboardInterrupt, SystemExit):
        cur.close()
        sock.close()

if __name__ == '__main__':
    Main()
