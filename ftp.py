
from ftplib import FTP
import sys
import os
SERVER = 'aigbusiness.in'
PORT = 21
BINARY_STORE = True

USER = 'policies@aigbusiness.in'
PASS = 'policy123'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UPLOAD_PATH = os.path.join(
    BASE_DIR,
    'static',
    'uploads'
)


def connect_ftp():
    # Connect to the server
    ftp = FTP()
    ftp.connect(SERVER, PORT)
    ftp.login(USER, PASS)

    return ftp


def upload_file(signaturename,name_3_emp_name):


    # Open the file
    try:
        upload_file_path = os.path.join(UPLOAD_PATH,name_3_emp_name)
        upload_file = open(upload_file_path, 'r')

        # get the name
        path_split = upload_file_path.split('/')
        final_file_name = str(signaturename) + str(path_split[len(path_split) - 1])

        # transfer the file
        print('Uploading ' + final_file_name + '...')

        ftp_connetion = connect_ftp()
        if BINARY_STORE:
            ftp_connetion = connect_ftp()
            ftp_connetion.storbinary('STOR ' + final_file_name, upload_file)
        else:
            # ftp_connetion.storlines('STOR ' + final_file_name, upload_file, print_line)
            ftp_connetion.storlines('STOR ' + final_file_name, upload_file)

        print('Upload finished.')

    except IOError:
        print("No such file or directory... passing to next file")
    return upload_file_path


# Take all the files and upload all
ftp_conn = connect_ftp()

for arg in sys.argv:
    upload_file(ftp_conn, arg)

