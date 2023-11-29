import os
import shutil
class FileExtensionSearchTool:
    def __init__(self, drive):
        self._drive = drive

    def Search(self, route, extension, dest):
        try:
            dirs = os.listdir(route)
        except:
            return

        for dir in dirs:
            sub_dir = os.path.join(route, dir)
            if os.path.isdir(sub_dir):
                self.Search(sub_dir, extension, dest)
            else:
                file_name = dir.split('.')
                if len(file_name) >= 2 and file_name[-1] == extension:
                    shutil.copy2(sub_dir, dest + '\\' + dir)

if __name__ == "__main__":
    search_tool = FileExtensionSearchTool('C')
    search_tool.Search('C:\\', 'txt')
        
    