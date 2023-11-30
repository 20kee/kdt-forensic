import shutil

class prefetch:
    def __init__(self):
        pass

    def prefetch_copy(self, folder):
        to_file_path = folder+'/prefetch/'
        from_file_path = 'C:\\Windows\\Prefetch'
        shutil.copytree(from_file_path, to_file_path)

def main(folder):
    prefetch_ = prefetch()
    prefetch_.prefetch_copy(folder)

if __name__ == '__main__':
    main('test')


