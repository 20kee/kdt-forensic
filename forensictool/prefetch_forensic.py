import shutil

class Prefetch:
    def __init__(self):
        pass

    def prefetch_copy(self, folder):
        from_file_path = 'C:\\Windows\\Prefetch'
        shutil.copytree(from_file_path, folder)

def main(folder):
    prefetch_ = Prefetch()
    prefetch_.prefetch_copy(folder)

if __name__ == '__main__':
    main('test')


