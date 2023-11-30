import shutil

class Srum:
    def __init__(self):
        pass

    def srum_copy(self, folder):
        from_file_path = 'C:\\Windows\\System32\\sru'
        shutil.copytree(from_file_path, folder)

def main(folder):
    srum_ = Srum()
    srum_.srum_copy(folder)

if __name__ == '__main__':
    main('test')


