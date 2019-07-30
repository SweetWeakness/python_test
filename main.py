import json
import os
import sys
import ftplib
from ftplib import FTP


def upload(host, username, password, filename, filetype):  # upload funtion
    ftp = ftplib.FTP(host, username, password)
    ftp.login()

    path = '/' + filename + '.' + filetype

    if filetype == 'txt' or filetype == 'html' or filetype == 'rst':
        ftp.storlines('/uploads' + path, open('.' + path, 'r'))
    else:
        ftp.storbinary('/uploads' + path, open('.' + path, 'rb'))


print('Print name of the file')  # getting info of the file
tmp = input().split('.')

if len(tmp) != 2:
    sys.exit('wrong input')

file_name = tmp[0]
file_type = tmp[1]
if not os.path.isfile('./' + file_name + '.json') or not os.path.isfile('./' + file_name + '.' + file_type):
    sys.exit('file(s) not found')


with open(file_name + '.json', "r") as read_file:  # starting to upload file
    data = json.load(read_file)
    upload(data["host"], data["username"], data["password"], file_name, file_type)
