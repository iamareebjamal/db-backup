import logging

from drive import DriveHelper

if __name__ == "__main__":
    logging.info('Starting Script')
    drive = DriveHelper()
    drive.upload_file('areeb.txt', 'Trying to upload file')

