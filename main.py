#https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/?ref=rp
from socket import *
import sys
import os
import base64
from PIL import Image
import io
import threading
from _thread import *
from configparser import ConfigParser
import datetime
import mimetypes
import pytz
import time
import stat

file = "serverconfig.ini"
config = ConfigParser()
config.read(file)
host = config['settings']['host']
port = config['settings']['port']
max = config['settings']['max connections']
buffer_size = config['settings']['buffer size']
log_file = config['settings']['logfile name'] 
print(host, port, max, buffer_size, log_file)

serverPort = int(port)
buffer_size = int(buffer_size)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(100)
print("HTTP server is running")

badreq = "HTTP/1.1 404 Not Found\n"
badreq += "Date: Thu, 22 Oct 2020 12:12:22 GMT\n"
badreq += "Server: HTTP/1.1 (Ubuntu)\n"
badreq += "Content-Length: 301\n"
badreq += "Connection: close\n"
badreq += "Content-Type: text/html; charset=iso-8859-1\n\n"
cookie = ""

def errorLogs(file, errornm):
	pid = os.getpid()
	pid = str(pid)

	current_time = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')))  
	level = " [core:error]"
	client = " [client 127.0.0.1]"
	filenm = ""
	if(file == ""):
		filenm = ""
	else:
		filenm =  " /" + file
	error = " "+ errornm
	temp = "["+ current_time + "]"+ level + "[ pid: " +pid +"]"+ client + error + filenm + "\n"
	f = open("error_logs.txt", "a")
	f.write(temp)
	f.close()

def accessLogs(var0, var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13):

	if(var1 == "/favicon.ico"):
		return
	remchar = ['/']
	for i in remchar:
		filename = var1.replace(i, "")
	size = ""
	try:
		size = os.path.getsize(filename)
		size = str(size)
	except FileNotFoundError:
		print("")
	accessLogs = "\n" + var4 + " "
	accessLogs += '"'+ var0 +  " "
	accessLogs += var1 + " "
	accessLogs += var2 + '" '
	status = str(200)
	accessLogs += status + " " + size + " "
	accessLogs += var6 + " "
	accessLogs += var7 
	accessLogs += var8
	accessLogs += var9
	accessLogs += var10
	accessLogs += var11
	accessLogs += var12
	accessLogs += var13 + "\n"
	f1 = open("accesslogs.txt", "a")
	f1.write(accessLogs)
	f1.close()

def setCookie(varcookie):
	with open('cookies.txt', 'r') as file:
		message = file.read()
		if varcookie in message:
			cookie = varcookie
		else:
			cookie = varcookie

	with open('cookies.txt', 'r+') as cookiefile:
		contents = cookiefile.read()
		if cookie in contents:
			pass
		else:
			cookiefile.write(cookie+"\n")
	return cookie

def getMethod(filename, connectionSocket, cookie):
	
	if(filename == "/favicon.ico"):
		return
	
	# remchar = ['/']
	
	# for i in remchar:
	# 	filename = filename.replace(i, "")
	# print(filename)
	filename = filename.replace("/", "", 1)
	isFile = os.path.isfile(filename)
	if(isFile == False):
		f = open("badrequest.html", "r")
		var = f.read()
		output = badreq + "\n" + var 
		connectionSocket.send(output.encode())
		return

	# if(isFile == True):
	# 	permission = os.access(filename, os.R_OK)
	# 	permissionLog = ""
	# 	if(permission == False):
	# 		permissionLog = "You Do not have Permissions to open the file"
	# 		errorLogs(filename, permissionLog)

	size = os.path.getsize(filename)
	size = str(size)
	contentType,fileEncoding = mimetypes.guess_type(filename)
	
	filestats = os.stat(filename)
	modificationTime = time.ctime(filestats [ stat.ST_MTIME ] )
	now = time.strftime("%c")
	string = "HTTP/1.1 200  OK\n"
	string += "Date: "+now+" \n"
	string += "Server: Apache/2.4.29(ubuntu)\n"
	string += "Last-Modified: "+modificationTime+"\n"
	string += "Content-Length: "+size+"\n"
	string += "Set-Cookie: "+cookie+"\n"
	string += "Connection: Keep-Alive\n"
	string += "Content-Type: "+ contentType + "; charset=iso-8859-1\n\n"
	
	
		
	if(filename.endswith(".png") or filename.endswith(".odt") or filename.endswith(".odp") or filename.endswith(".PDF") or filename.endswith(".mp4") or filename.endswith(".mp3")):
		with open(filename, "rb") as format:
			data1 = format.read()
		connectionSocket.send(string.encode())
		connectionSocket.send(data1)
		return



	elif(filename.endswith(".txt")):
		f = open(filename, "r")
		lines = f.read()
		output = string + lines
		connectionSocket.send(output.encode())
		return


	else:
		with open(filename, "rb") as otherFormat:
			data1 = otherFormat.read()
		connectionSocket.send(string.encode())
		connectionSocket.send(data1) 

def headMethod(filename, connectionSocket, cookie):
	if(filename == "/favicon.ico"):
		return
	# remchar = ['/']
	# for i in remchar:
	# 	filename = filename.replace(i, "")
	filename = filename.replace("/", "", 1)
	isFile = os.path.isfile(filename)
	if(isFile == False):
		output = badreq 
		connectionSocket.send(output.encode())
		return
	size = os.path.getsize(filename)
	size = str(size)
	contentType,fileEncoding = mimetypes.guess_type(filename)

	filestats = os.stat(filename)
	modificationTime = time.ctime(filestats [ stat.ST_MTIME ] )
	now = time.strftime("%c")
	string = "HTTP/1.1 200 OK\n"
	string += "Date: "+now+"\n"
	string += "Server: Apache/2.4.29(ubuntu)\n"
	string += "Last-Modified: "+modificationTime+"\n"
	string += "Content-Length: "+size+"\n"
	string += "Set-Cookie: "+cookie+"\n"
	string += "Connection: close\n"
	string += "Content-Type: "+ contentType + "; charset=iso-8859-1\n\n"
	
	if(filename.endswith(".png") or filename.endswith(".txt") or filename.endswith(".mp4") or filename.endswith(".mp3") or filename.endswith(".odp") or filename.endswith(".odt") or filename.endswith(".PDF")):
		with open(filename, "rb") as format:
			data1 = format.read()
		connectionSocket.send(string.encode())

	elif(filename.endswith(".txt")):
		f = open(filename, "r")
		lines = f.read()
		f.close()
		output = string 
		connectionSocket.send(output.encode())
		return

	else:
		with open(filename, "rb") as otherFormat:
			data1 = otherFormat.read()
		connectionSocket.send(string.encode())

def deleteMethod(filename, connectionSocket, cookie):
	if(filename == "/favicon.ico"):
		return
	# remchar = ['/']
	# for i in remchar:
	# 	filename = filename.replace(i, "")
	filename = filename.replace("/", "", 1)
	isFile = os.path.isfile(filename)
	if(isFile == False):
		f = open("badrequest.html", "r")
		var = f.read()

		#status = "400"
		f.close()
		output = badreq + var
		connectionSocket.send(output.encode())
		return
	size = os.path.getsize(filename)
	size = str(size)
	
	contentType,fileEncoding = mimetypes.guess_type(filename)

	filestats = os.stat(filename)
	modificationTime = time.ctime(filestats [ stat.ST_MTIME ] )
	now = time.strftime("%c")

	string = "HTTP/1.1 200 OK\n"
	string += "Date: "+now+"\n"
	string += "Server: Apache/2.4.29(ubuntu)\n"
	string += "Last-Modified: "+modificationTime+"\n"
	string += "Content-Length: "+size+"\n"
	string += "Set-Cookie: "+cookie+"\n"
	string += "Connection: close\n"
	string += "Content-Type: "+ contentType + "; charset=iso-8859-1\n\n"
	
	if(filename.endswith(".txt") or filename.endswith(".png") or filename.endswith(".deb") or filename.endswith(".jpg") or filename.endswith(".mp4") or filename.endswith(".mp3") or filename.endswith(".odp") or filename.endswith(".odt") or filename.endswith(".tar.xz")):
		os.remove(filename)
		string += "\n"
		string += "URL Deleted"
		output = string
		connectionSocket.send(output.encode())
	'''if(filename.endswith(".png")):
		os.re
		output = string + b
		connectionSocket.send(output)
		return
	'''
def putMethod(filename, body, connectionSocket, cookie):
	if(filename == "/favicon.ico"):
		return
	#remchar = ['/']
	size = 0
	size = str(size)
	# for i in remchar:
	# 	filename = filename.replace(i, "")
	filename = filename.replace("/", "", 1)
	isFile = os.path.isfile(filename)

	#filestats = os.stat(filename)
	#modificationTime = time.ctime(filestats [ stat.ST_MTIME ] )
	now = time.strftime("%c")
	#isFile = os.path.isfile(filename)
	'''if(isFile == False):
		f = open("badrequest.html", "r")
		var = f.read()

		#status = "400"
		f.close()
		output = badreq + var
		connectionSocket.send(output.encode())
		return'''
	if(isFile == False):
		statusCode = "201 created"
		size = 0
		size = str(size)
		modificationTime = now
	if(isFile == True):
		size = os.path.getsize(filename)
		size = str(size)
		statusCode = "200 OK"
		filestats = os.stat(filename)
		modificationTime = time.ctime(filestats [ stat.ST_MTIME ] )
		now = time.strftime("%c")
	if(filename.endswith(".mp4")):
		contentType = "video/mp4"
	if(filename.endswith(".mp3")):
		contentType = "audio/mpeg"
	if(filename.endswith(".png")):
		contentType = "Image/png"
	if(filename.endswith(".txt")):
		contentType = "text/html"
	
	string = "HTTP/1.1 "+statusCode+ " \n"
	string += "Date: "+now+"\n"
	string += "Server: Apache/2.4.29(ubuntu)\n"
	string += "Last-Modified: "+modificationTime+"\n"
	string += "Content-Length: "+size+"\n"
	string += "Set-Cookie: "+cookie+"\n"
	string += "Connection: close\n"
	string += "Content-Type: "+ contentType + "; charset=iso-8859-1\n\n"
	if(isFile == False):
		f = open(filename, "w")
		f.write(body)
		f.close()
		output = string 
		connectionSocket.send(output.encode())
		return
		
	
	if(isFile == True):
		f = open(filename, "w")
		f.write(body)
		f.close()
		output = string 
		connectionSocket.send(output.encode())
	
def postMethod(filename, body, connectionSocket, cookie):
	if(filename == "/favicon.ico"):
		return
	# remchar = ['/']
	# for i in remchar:
	# 	filename = filename.replace(i, "")
	filename = filename.replace("/", "", 1)
	isFile = os.path.isfile(filename)
	if(isFile == False):
		f = open("badrequest.html", "r")
		var = f.read()

		#status = "400"
		f.close()
		output = badreq + var
		connectionSocket.send(output.encode())
		return
	filestats = os.stat(filename)
	modificationTime = time.ctime(filestats [ stat.ST_MTIME ] )
	now = time.strftime("%c")

	
	size = os.path.getsize(filename)
	size = str(size)
	if(filename.endswith(".mp4")):
		contentType = "video/mp4"
	if(filename.endswith(".mp3")):
		contentType = "audio/mpeg"
	if(filename.endswith(".png")):
		contentType = "Image/png"
	if(filename.endswith(".txt")):
		contentType = "text/html"
	string = "HTTP/1.1 200 OK\n"
	string += "Date: "+ now+"\n"
	string += "Server: Apache/2.4.29(ubuntu)\n"
	string += "Last-Modified: "+modificationTime+"\n"
	string += "Content-Length: "+size+"\n"
	string += "Set-Cookie: "+cookie+"\n"
	string += "Connection: close\n"
	string += "Content-Type: "+ contentType + "; charset=iso-8859-1\n\n"
	if(filename.endswith(".txt")):
		f = open(filename, "a")
		f.write(body)
		f.close()
		# string += "\n"
		# string += "Data processed"
		output = string 
		connectionSocket.send(output.encode())
def getheaders(new_data):
    flag, count = 0, 0
    ifmodified = 'If'
    for i in new_data:
        if ifmodified in i:
            ifmodifiednew = i
            flag = 1
    if flag == 1:
        for i in ifmodifiednew:
            count = count + 1
            if i == ':':
                ifmodifiednew = ifmodifiednew[count + 1:]
                break
        return ifmodifiednew
    if flag == 0:
        ifmodifiednew = 0
        return ifmodifiednew


def splitheaders(data):
    data_for_post = data
    new_data = data.splitlines()
    lines = new_data[0].split()
    method_h = lines[0]
    url_h = lines[1]
    url_h1 = url_h
    for i in url_h:
        if i == '/':
            url_new = url_h.split('/')
    url_h = url_new[len(url_new) - 1]
    version_h = lines[2]
    modified_since = getheaders(new_data)
    return method_h, url_h, version_h, modified_since, url_h1, data_for_post, new_data[0]
def myThread(connectionSocket):
	try:
		header = connectionSocket.recv(buffer_size).decode()
			
	except socket.error:
		print("Server Stopped")
	method_h, url_h, version_h, modified_since, url_h1, data_for_post, new_data_statusline = splitheaders(header)
	print(url_h1)
	sections = header.split()
	filename = url_h1	
	# print(sections[4])#localhost:portno
	# print(sections[1])
	try:
		varcookie = sections[4]
	except IndexError:
		print("")
	
	
	if(filename == "/favicon.ico"):
		return

	# remchar = ['/']
	
	# for i in remchar:
	# 	filename = filename.replace(i, "")
	filename = filename.replace("/", "", 1)
	isFile = os.path.isfile(filename)
	if(isFile == False):
		existLog = "File does not exist"
		exist = False

		f = open("badrequest.html", "r")
		var = f.read()
		
		#status = "400"
		f.close()
		output = badreq + var
		#errorLogs(filename, existLog)
		connectionSocket.send(output.encode())
		errorLogs(filename, existLog)
		return



	if(isFile == True):
		permission = os.access(filename, os.R_OK)
		permissionLog = ""
		if(permission == False):
			permissionLog = "You Do not have Permissions to open the file"
			errorLogs(filename, permissionLog)
			return
	
	cookie = setCookie(sections[4])
	if(sections[0] == "GET"):
		status = 200
		getMethod(url_h1, connectionSocket, cookie)

	if(sections[0] == "HEAD"):
		status = 200
		headMethod(url_h1, connectionSocket, cookie)

	if(sections[0] == "PUT"):
		status = 201
		contents = sections[27:29]
		#print(contents)
		n = len(contents)
		body = ""
		print(n)
		i = 0
		for i in range(0, n):
			body += contents[i] + " "
			i = i + 1
		print(body)
		putMethod(url_h1, body, connectionSocket, cookie)
		
	if(sections[0] == "DELETE"):
		status = 200
		deleteMethod(url_h1, connectionSocket, cookie)
		
	if(sections[0] == "POST"):
		status = 200
		#print(sections[30:32])
		contents = sections[27:29]
		n = len(contents)
		body = ""
		print(n)
		i = 0
		for i in range(0, n):
			body += contents[i] + " "
			i = i + 1
		print(body)
		postMethod(url_h1, body, connectionSocket, cookie)
	accessLogs(sections[0], sections[1], sections[2], sections[3], sections[4], sections[5], sections[6], sections[7], sections[8], sections[9], sections[10], sections[11], sections[12], sections[13])

def main():
	while True:
		try:
			connectionSocket, addr = serverSocket.accept()
	
			threading.Thread(target = myThread, args = (connectionSocket, ), daemon = True).start()
		except KeyboardInterrupt:
			print("Server Stopped")
			quit()

		
	connectionSocket.close()

if __name__ == '__main__':
	n = len(sys.argv)
	if(n < 2):
		error = "Attempt to start the server failed"
		print("Attempt to start the server failed")
		print("Start the server by python3 main.py start")

		file = ""
		errorLogs(file, error)
	elif(sys.argv[1] == 'start'):
		main()
	else:
		print("Start the server by python3 main.py start")
        
