import logging

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class DriveHelper:
    folder_name = 'db_backup'
    folder_mime_type = 'application/vnd.google-apps.folder'
    backup_folder = None

    def __init__(self):
        self.logger = logging.getLogger('gdrive')
        # self.logger.setLevel(logging.DEBUG)

        self.logger.info('Authenticating Google Drive...')
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        self.drive = GoogleDrive(gauth)
        self.logger.info('Authenticated')
        self.backup_folder = self.get_backup_folder()

    def get_backup_folder(self):
        if self.backup_folder:
            return self.backup_folder
        self.logger.info('Checking if backup directory exists...')
        query = f"title='{self.folder_name}' and 'root' in parents and " \
                f"mimeType='{self.folder_mime_type}' and trashed=false"
        file_list = self.drive.ListFile({
            'q': query
        }).GetList()
        if len(file_list) < 1:
            self.logger.warning("Backup folder doesn't exist.")
            self.logger.info('Creating backup directory...')
            backup_folder = self.drive.CreateFile({
                'title': self.backup_folder,
                'mimeType': self.folder_mime_type
            })
            backup_folder.Upload()
            self.logger.info('Folder Created with ID ' + backup_folder['id'])
        else:
            backup_folder = file_list[0]
            self.logger.info('Folder Exists with ID ' + backup_folder['id'])

        return backup_folder

    def upload_file(self, title: str, content: str):
        self.logger.info('Uploading file...')
        file = self.drive.CreateFile({
            'title': title,
            'parents': [
                {
                    'kind': 'drive#fileLink',
                    'id': self.backup_folder['id']
                }
            ]
        })
        file.SetContentString(content)
        file.Upload()
        self.logger.info('Uploaded')
        return file
