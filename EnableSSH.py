#!/user/bin/env python

import telnetlib
import time
import getpass

#Define telnet parameters and prompt for them, password using getpass
username = raw_input("Enter username (defalut = adam1) :") or "adam1"
password = getpass.getpass("Enter password (default = adam1) :") or "adam1"

#define config files and server list files
cmd_file1 = raw_input("Enter 1st command file name and extension (default = ./commands1.txt) : ") or "./commands1.txt"
srv_file = raw_input("Enter Server List file name and extension (default = ./servers.txt) : ") or "./servers.txt"  

#Open telnet connection to devices
def open_telnet_conn(ip):
#    #Change exception message

    try:                   
        #Specify the Telnet port (default is 23)
        port = 23        

        #Specify the connection timeout in seconds for blocking opperations, Like the connection attempt
        connection_timeout = 5        

        #Specity the timout in seconds, Read until the string is found or until the timout has passed
        reading_timeout = 5        

        #Logging into the device
        connection = telnetlib.Telnet(ip, port, connection_timeout)        

        ###Waiting to be asked for a username
        router_output = connection.read_until("Username:", reading_timeout)		
        #Enter the password when asked and add "\n" for Enter
        connection.write(username + "\n")
        time.sleep(1)        

        ###Waiting to be asked for a password
        router_output = connection.read_until("Password:", reading_timeout)		
        #Enter the password when asked and add "\n" for Enter
        connection.write(password + "\n")
        time.sleep(1)        

        #Setting terminal length for entire output - disabling pagination
        connection.write("terminal length 0\n")
        time.sleep(1)        

        #Entering global config mode
        connection.write("\n")
        connection.write("configure terminal\n")
        time.sleep(1)            

        #Open user selected file for reading
        selected_cmd_file1 = open(cmd_file1, "r")
        
        #Starting from the beginning of the file
        selected_cmd_file1.seek(0)
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file1.readlines():
            connection.write(each_line)
            time.sleep(2)
       
        #Closing the file
        selected_cmd_file1.close()
        
        #Test for reading command output
        router_output = connection.read_very_eager()
        print router_output
    except IOError as err:
        print ("Command File or Sever File data error!: {0}".format(err))


#Defining the server details
selected_srv_file = open(srv_file, "r")
selected_srv_file.seek(0)

#Executing telnet script on a per server basis
for srv_line in selected_srv_file.readlines():
    #Display current switch to configure
    print("Connecting to ") + (srv_line)
    #execute script
    open_telnet_conn(srv_line)
