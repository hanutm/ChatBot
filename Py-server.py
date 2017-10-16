## ChartServer code using sockets

### tasks left -1.creating chatroom list
#		2.adding people to chatrooms
#		3.Error Handling


import socket
from threading import Thread
import random

def check_msg(msg):
	if (msg.find('JOIN_CHATROOM'.encode('utf-8'))+1):
		return(1)	
	elif (msg.find('LEAVE_CHATROOM'.encode('utf-8'))+1):
		return(2)
	elif (msg.find('DISCONNECT'.encode('utf-8'))+1):
		return(3)
	elif (msg.find('CHAT:'.encode('utf-8'))+1):
		return(4)	
	else:
		return(5)

def join(conn_msg,csock):
	gname = conn_msg.find(':'.encode('utf-8'))+2
	gname_end = conn_msg.find('\n'.encode('utf-8'))-1
	groupname = conn_msg[gname:gname_end]

	cname = conn_msg.find('CLIENT_NAME'.encode('utf-8'))+13
	cname_end = conn_msg.find(' '.encode('utf-8'),cname)
	clientname = conn_msg[cname:cname_end]
	
	if groupname == 'g1' :
		g1_clients.append(clThread)
		rID = 1001
	elif groupname == 'g2' :
		g2_clients.append(clThread)
		rID = 1002

	#sending ackowledgement
	response = "JOINED_CHATROOM: ".encode('utf-8') + groupname+ "\n".encode('utf-8')
	response += "SERVER_IP: \n".encode('utf-8')
	response += "PORT: \n".encode('utf-8')
	response += "ROOM_REF: ".encode('utf-8') + str(rID).encode('utf-8') +'\n'.encode('utf-8')
	response += "JOIN_ID: ".encode('utf-8') + str(clThread.uid).encode('utf-8')   

	csock.send(response)
	return groupname,clientname

def discon(csock):
	response = "DISCONNECT: \n"
	response += "PORT: \n"
	response += "CLIENT_NAME: " + clThread.clientid
	csock(response)
	clThread.exit()

def leave():
	pass

def chat(conn_msg,csock):
	chat_msg_start = conn_msg.find('MESSAGE:'.encode('utf-8')) + 9
	chat_msg_end = conn_msg.find('\n\n'.encode('utf-8'),chat_msg_start) - 1	

	chat_msg = conn_msg[chat_msg_start:chat_msg_end]

	grp_start = conn_msg.find('CHAT:'.encode('utf-8')) + 5
	grp_end = conn_msg.find('\n'.encode('utf-8'), grp_start) - 1

	group_name = conn_msg[grp_start:grp_end]
	
	chat_text = 'CHAT:'.encode('utf-8') + chat_msg + '\n'.encode('utf-8')
	chat_text += 'CLIENT_NAME:'.encode('utf-8') +str(clThread.clientid).encode('utf-8')
	chat_text += 'MESSAGE: ' + chat_msg.encode('utf-8') 

	if group_name == g1:
		for x in g1:
			(g1[x].socket).send(chat_text)
	elif group_name == g2:
		for x in g2:
			(g2[x].socket).send(chat_text)
	
class client_threads(Thread):

	def __init__(self,ip,port,socket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.chatroom =[] 
		self.socket = socket
		self.uid = random.randint(1000,2000)

	def run(self):
		while True:
			conn_msg = csock.recv(1024)
			cflag = check_msg(conn_msg)
#			print(conn_msg)
			if cflag == 1 :
				 self.roomname,self.clientid = join(conn_msg,csock)
			elif cflag == 2 : leave()
			elif cflag == 3 : discon(csock)
			elif cflag == 4 : chat()
			else : pass					 #error code for incorrect message	
#			print(self.name)
			self.chatroom.append(self.roomname)
#			print('roomnames')
#			print(self.chatroom)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 50000
server.bind((host,port))
print(host)
thread_count = [] 

g1_clients = []
g2_clients = []


while True:
	server.listen(4)
	(csock,(ip,port)) = server.accept()

	print("Connected to ",port,ip)
	#monitoring connections

	clThread = client_threads(ip,port,csock)
	clThread.start()
	thread_count.append(clThread)
	print("Threads :")
	print(thread_count)
