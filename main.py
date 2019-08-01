import json
import os
import sys
import ftplib
from threading import Thread


class FTP_server:

    def __init__(self, host, username, password):
        self.ftp = ftplib.FTP()
        self.state = 'connected'
        try:
            self.ftp.connect(host)
            self.ftp.login(username, password)
        except ftplib.error_perm:
            print('Invalid username or password')
        except ftplib.error_reply:
            print('Unexpected reply is received from the server')
        except ftplib.error_proto:
            print('Reply is received from the server that does not fit'
                  'the response specifications of the File Transfer Protocol,'
                  'i.e. begin with a digit in the range 1–5')
        except ftplib.error_temp:
            print('Error code signifying a temporary error'
                  '(response codes in the range 400–499) is received')
        finally:
            self.state = 'disconnected'

    def upload(self, filename, filetype):  # upload function
        if self.state == 'disconnected':
            print('No connection')
            return

        path = '/' + filename + '.' + filetype

        file = open('.' + path, 'rb')
        self.ftp.storbinary('STOR /uploads' + path, file)
        file.close()

    def close(self):
        self.ftp.close()


def upload_on_ftp(file):
    tmp = file.split('.')

    if len(tmp) != 2:
        print('Wrong input (' + file + ')')
        return

    file_name = tmp[0]
    file_type = tmp[1]
    if not os.path.isfile('./' + file_name + '.json') or \
            not os.path.isfile('./' + file_name + '.' + file_type):
        print('File(s) not found (' + file + ')')
        return

    with open(file_name + '.json', "r") as read_file:  # starting to upload file
        data = json.load(read_file)

        con = FTP_server(data["host"], data["username"], data["password"])
        con.upload(file_name, file_type)
        con.close()


if __name__ == '__main__':

    print('Print several files ("file.type") through the gap')  # getting info of the file

    arr = input().split(' ')

    for f in arr:
        print(f)
        thread = Thread(target=upload_on_ftp(f))
        thread.start()
        thread.join()
