
host = '45.9.43.17'
user = 'root'
secret = 'fZ^xh6a4#FYV'
port = 22
import paramiko

# Update the next three lines with your
import time
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=secret)
channel = client.invoke_shell()
time.sleep(0.2)
