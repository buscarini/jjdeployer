#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ftplib import FTP
import os
import sys
import getpass
import askpass

def uploadFiles(ftp,files):
    for file in files:
        name = os.path.basename(file)        
        if not os.path.exists(file):
            print "Error: file " + file + " doesn't exist"
            exit(1)
        
        if os.path.isdir(file):
            print "mkdir " + name            
            if not name in ftp.nlst():
                ftp.mkd(name)

            ftp.cwd(name)
            
            children = os.listdir(file)
            subfiles = []
            for child in children:
                subfiles.append(os.path.join(file,child))    

            uploadFiles(ftp,subfiles)
            
            ftp.cwd("..")
        else:    
            print "upload " + file
            ftp.storbinary(('STOR ' + name).encode('utf-8'), open(file, 'rb'))
    

if len(sys.argv)<5:
    sys.exit('Usage: %s "keychain_service" "keychain_account" "server" "port" "path" [files]' % sys.argv[0])
    
params = sys.argv[1:]
service = params.pop(0)
account = params.pop(0)
server = params.pop(0)
port = params.pop(0)
path = params.pop(0)
files = params

passw = askpass.findPass(service,account)
if passw==None:
    sys.exit("Please create the password first or allow access")

print "connect to server " +  server + " port " + port
ftp = FTP()
ftp.connect(server,port)
ftp.login(account,passw)
ftp.cwd('/')

folders = []
while 1:
    path, folder = os.path.split(path)
    if folder != "":
        folders.append(folder)
    else:
        if path != "":
            folders.append(path)
        break
        
folders.reverse()

for folder in folders:
    print "mkdir " + folder

    if not folder in ftp.nlst():
        ftp.mkd(folder)
        
    ftp.cwd(folder)


uploadFiles(ftp,files)

    
ftp.quit()