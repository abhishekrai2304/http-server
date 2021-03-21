# https://realpython.com/python-requests/
# Writing a testing program
import requests
import sys
port = int(sys.argv[1])
url = 'http://127.0.0.1:' + str(port)
data = {'key': 'abhi',
                'value': '3232323'}

getPath = "/Report.PDF"
'''Basic GET reqest'''
try:
    print("-----------------Testing GET request----------------")
    response = requests.get(url + getPath)
    
    if not response:
        print("Failed to give response!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')


putPath = "/test.txt"
try:
    print("\n-----------------Testing PUT request-----------------")
    response = requests.put(url+putPath, json = data)
    if not response:
        print("Failed to give response!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

delPath = "/hello.txt"
try:
    print("\n----------------Testing DELETE request---------------")
    response = requests.delete(url + delPath)
    if not response:
        print("Failed to give response!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

headPath = "/kabir.mp3"
try:
    print("\n-----------------Testing HEAD request----------------")
    response = requests.head(url + headPath)
    if not response:
        print("Failed to give response!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')


postPath = "/test.txt"
try:
    print("\n----------------Testing POST request----------------")
    response = requests.post(url+postPath, json = data)
    if not response:
        print("Failed to give response!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}') 