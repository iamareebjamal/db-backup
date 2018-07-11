import datetime
import json
import os


class FileHelper:
    last_index_time = None

    def __init__(self):
        print('Checking if backup directory exists...')
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

        self.backup_folder = os.path.join(self.current_dir, 'db_backup')
        if not os.path.isdir(self.backup_folder):
            print('Folder not found. Creating new folder...')
            os.makedirs(self.backup_folder)
            print('Folder created')
        print('Getting last indexed time...')
        self.index_file = os.path.join(self.backup_folder, 'index.json')
        if not os.path.isfile(self.index_file):
            self.save_last_index_time(datetime.datetime.utcfromtimestamp(0))
        else:
            self.last_index_time = self.get_last_index_time()

    def get_last_index_time(self):
        if self.last_index_time:
            return self.last_index_time
        with open(self.index_file, 'r') as fi:
            last_index_time = datetime.datetime.fromtimestamp(json.loads(fi.read())['last_indexed_time'])
        return last_index_time

    def save_last_index_time(self, date=datetime.datetime.now()):
        self.last_index_time = date
        with open(self.index_file, 'w') as fi:
            fi.write(json.dumps({
                'last_indexed_time': self.last_index_time.timestamp()
            }))

    def get_backups(self):
        return sorted(
            list(
                map(lambda name: {'file': name, 'time': datetime.datetime.fromtimestamp(os.path.getmtime(name))},
                    filter(lambda file: os.path.getsize(file) > 0,
                           map(lambda name: os.path.join(self.backup_folder, name),
                               filter(lambda name: name.endswith('.txt'),
                               os.listdir(self.backup_folder)))))),
            key=lambda item: item['time'])

    def get_new_backups(self):
        return list(filter(lambda item: item['time'] > self.last_index_time, self.get_backups()))


if __name__ == "__main__":
    fh = FileHelper()
    print(fh.get_new_backups())
