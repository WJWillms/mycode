#!/usr/bin/env python3

from paramiko import SSHClient
from paramiko.client import AutoAddPolicy

def main():
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        #client.connect('10.10.2.3', username='bender', password='Alta3') , key_filename='./KEYNAME.pem')
        client.connect('10.10.2.3', username='bender', password='alta3')
        stdin, stdout, stderr = client.exec_command('ls -l /tmp')
        output = stdout.read()
        print(output.decode())
if __name__ == '__main__':
    main()

