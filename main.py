import json
import os
import sys
import ftplib


class FTPserver:

    def __init__(self, host, username, password):
        self.ftp = ftplib.FTP(host, username, password)

    def upload(self, filename, filetype):  # upload function
        path = '/' + filename + '.' + filetype

        file = open('.' + path, 'rb')
        self.ftp.storbinary('STOR /uploads' + path, file)
        file.close()

    def close(self):
        self.ftp.close()


if __name__ == '__main__':

    print('Print "file.type" ')  # getting info of the file
    tmp = input().split('.')

    if len(tmp) != 2:
        sys.exit('wrong input')

    file_name = tmp[0]
    file_type = tmp[1]
    if not os.path.isfile('./' + file_name + '.json') or not os.path.isfile('./' + file_name + '.' + file_type):
        sys.exit('file(s) not found')

    with open(file_name + '.json', "r") as read_file:  # starting to upload file
        data = json.load(read_file)

        con = FTPserver(data["host"], data["username"], data["password"])
        con.upload(file_name, file_type)
        con.close()


