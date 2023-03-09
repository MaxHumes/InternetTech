import socket
import signal
import sys
import random

from enum import Enum
class Status(Enum):
    LOGIN = 1
    FAILURE = 2
    SUCCESS = 3

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "password" value = "new" />
   <input type = "submit" value = "Click here to Change Password" />
   </form>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % (port, port)

new_password_page = """
   <form action="http://localhost:%d" method = "post">
   New Password: <input type = "text" name = "NewPassword" /> <br/>
   <input type = "submit" value = "Submit" />
</form>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print "Here is the", tag
    print "\"\"\""
    print value
    print "\"\"\""
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users
def lines_to_dict(file):
    new_dict = {}
    for line in file:
        tup = line.split()
        if len(tup) > 1:
            new_dict[tup[0]] = tup[1]
    return new_dict
with open('passwords.txt', 'r') as pass_file, open('secrets.txt','r') as secret_file:
    pass_dict = lines_to_dict(pass_file)
    secret_dict = lines_to_dict(secret_file)

#dictionary mapping cookies to users
cookies_dict = {}

### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions
    
    #returns cookie from header and empty string if there is none
    def parse_HTTP_header_for_cookie(header):
        for line in header.splitlines():
            field_val = line.split(':')
            if len(field_val) > 1:
                if field_val[0] == 'Cookie':
                    token_val = field_val[1].split('=')
                    if len(token_val) > 1:
                        return token_val[1]
        return ''
    #returns status code, username, password triple
    #username and password returned as emptystrings on failure
    def parse_HTTP_body(content):
        #split body by fields
        body_fields = content.split('&')
        if len(body_fields) == 1:
            if not body_fields[0]:
                return Status.LOGIN, '', ''
            return Status.FAILURE, '', ''
        else:
            username = ''
            password = ''
            #loop through fields in request body
            for field in body_fields:
                #determine field name and value
                field_val = field.split('=')
                if len(field_val) > 1:
                    if field_val[0] == 'username':
                        username = field_val[1]
                    elif field_val[0] == 'password':
                        password = field_val[1]
                    else:
                        return Status.FAILURE, '', ''
                else:
                    return Status.FAILURE, '', ''
            
            #authenticate password       
            if not(username in pass_dict and password == pass_dict[username]):
                return Status.FAILURE
            return Status.SUCCESS, username, password        
    # You need to set the variables:
    # (1) `html_content_to_send` => add the HTML content you'd
    # like to send to the client.
    # Right now, we just send the default login page.
    # But other possibilities exist, including
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page    
    
    html_content_to_send,headers_to_send='',''
    cookie = parse_HTTP_header_for_cookie(headers)
    if cookie and cookie in cookies_dict:
        html_content_to_send = success_page + secret_dict[cookies_dict[cookie]]
    elif cookie and not(cookie in cookies_dict):
        html_content_to_send = bad_creds_page
    else:
        #determine html content to send
        status, username, password = parse_HTTP_body(body)
        if status == Status.LOGIN:
            html_content_to_send = login_page
        elif status == Status.FAILURE:
            html_content_to_send = bad_creds_page
        elif status == Status.SUCCESS:
            html_content_to_send = success_page + secret_dict[username]
            # (2) `headers_to_send` => add any additional headers
            # you'd like to send the client?
            rand_val = random.getrandbits(64)
            token = str(rand_val)
            cookies_dict[token] = username 
            headers_to_send = 'Set-Cookie: token=' + token + '\r\n'
            
            
    if(body) == 'password=new':
            html_content_to_send = new_password_page
    if(body[:11]) == 'NewPassword':
            newPass = body[12:len(body)]
            pass_dict[username] = newPass
            html_content_to_send = success_page
            print(pass_dict)

            with open('passwords.txt', 'w') as file:
                for key, value in pass_dict.items():
                    file.write("%s %s\n" % (key, value))
    
    

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    
    print "Served one request/connection!"
    print

# We will never actually get here.
# Close the listening socket
sock.close()
