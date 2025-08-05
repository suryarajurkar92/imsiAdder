
# This python script is used for adding the list of IMSIs automatically to MCPTT platform
# This functionality will avoid the effort from using curl command (for each IMSI)
# to push the IMSI information to MCPTT platform
# Details regarding Server IP and respective access is hidden due to security reasons

import paramiko
import csv
import time
import tkinter as tk
from tkinter import filedialog

# Contact Technical Projects team for accessing Username and Password 
# CSC Server Access
hostname = "Enter the host IP address"
port = "Enter the respective port"
username = "****"
password = "****"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    # this saves as a known hostnames for the user

# Select a IMSI data file
input_data = tk.filedialog.askopenfilename(title="Select a IMSI data file")
with open(input_data, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    #print(rows)

try:
    client.connect(hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('ls -la')

    print(stdout.read().decode())
    print(stderr.read().decode())


    for row in rows:
        
        i = row['IMSI']
        p = row['Product']

        print(f"Curl Command Running for {i} with Product {p}")
        curl = f"curl -k --include -X PUT 'https://10.90.6.153:2359/jdms/v2/qos/sim/{i}/product/{p}'"   
        
        stdin, stdout, stderr = client.exec_command(curl)

         
        """ print(stdout.read().decode())
        print(stderr.read().decode()) """

        output = stdout.read().decode()
        error = stderr.read().decode()

        if "200 OK" in output:
            print(f"IMSI {i} is provisioned!")
        else:
            print(f"{output.strip()} Fail!!! IMSI {i} is not provisioned!")
        
        
        time.sleep(2)     # Wait for 2 seconds before sending the next IMSI provisioning request.


finally:
    client.close()

