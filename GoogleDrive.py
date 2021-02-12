# import os
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth
# drive = GoogleDrive(gauth)
#
# file1 = drive.CreateFile({'title':'Hello.txt'})
# file1.SetContentFile('Co')
#
# file1.Upload()

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '1fgOX8hScgzxXEADZX9_yO462MMYtrKlJ'
file_names = ['Covid19.XLSX', 'covid2019.html']
mime_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/html']

for file_name, mime_type in zip(file_names, mime_types):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(filename=file_name, mimetype=mime_type)

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

# print(dir(service))

# http://localhost:8080