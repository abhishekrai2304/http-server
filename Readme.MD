Http Server Implementation in Python

To run the project use the ./start.sh start

To stop the project use Ctr + C

Http Server Features-

It contains the following methods:-

1)GET :- 
I have implemented GET like it works in Apache and it works for all the file formats.

2)POST:-
In the Post method, the data that the body of the Request contains is written in .txt file.

3)DELETE:-
In the delete method we check both the conditions that it is present or not and accordingly give response to the user.

4)HEAD:-
Its is same as GET method excpet we donot send the body to the user.

5)PUT:-
In PUT, the data sent in the request body will be updated or created on server.

Server Configuration-:
	The server necessary configuration is present in serverconfig.ini and it is read in the main file and accordingly its values are set.

Log Files:-
	I have implemented 2 log files:-
	1)accessLogs.txt - In this all the requests made to the server are listed, as like the apache does.
	2)errorLogs.txt - All the errors are reported in this file.

automatedTest.py :-
	It contains automatic testing of all the methods of Http server.

cookies.txt -:
	It contains record of all the cookies created by server for a client.






