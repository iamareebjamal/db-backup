import datetime

from drive import DriveHelper

from local import FileHelper

if __name__ == "__main__":
    print('Starting Script')
    file_helper = FileHelper()

    backups = file_helper.get_new_backups()
    backup_count = len(backups)

    drive = DriveHelper(expiry_time=datetime.timedelta(minutes=20))
    for idx, backup in enumerate(backups):
        print(f"Uploading file {backup['file']} {idx + 1} of {backup_count}...")
        drive.upload_file_by_path(backup['file'])

    file_helper.save_last_index_time()
    drive.purge_stale_backups()
