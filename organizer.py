import os, shutil
import filetype

class FileOrganizer:
    """
    target - the folder want to be organized
    destinatin - where should store the files
    should provide abs path
    """
    def __init__(self, target=None, destination=None):
        _mainFolder = "Organized"

        if target:
            self.location = target
        else:
            self.location = os.path.join(os.path.expanduser("~"), "Downloads")

        if destination:
            self.dest = os.path.join(destination, _mainFolder)
        else:
            self.dest = os.path.join(os.path.expanduser("~"), "Downloads", _mainFolder)

    def __readLocation(self):
        allFiles = os.listdir(self.location)
        files = [f for f in allFiles if os.path.isfile(self.location + "/" + f)]
        return files
    
    # this will categorize files by file extintion
    def categorizeByExt(self, files):
        output = {}
        for file in files:
            ext = file.split('.')[-1]
            if ext in output:
                output[ext].append(file)
            else:
                output[ext] = [file]
        
        return output

    # this will categorize files by file type (img, video, etc)
    def categorizeByType(self, files):
        output = {"Others": []}
        for file in files:
            type = filetype.guess(self.location + '/' + file)
            if type is not None:
                id = type.mime.split('/')[0]
                if id in output:
                    output[id].append(file)
                else:
                    output[id] = [file]
            else:
                output["Others"].append(file)
        
        return output

    # this will move the given file to the destination folder
    def __moveFile(self, file, folder):
        src = os.path.join(self.location, file) 
        dest = os.path.join(self.dest, folder)
        shutil.move(src, dest)

    # this will create folder in the destination
    def __createFolders(self, folders):
        for folder in folders:
            absDest = os.path.join(self.dest, folder)
            os.makedirs(absDest, exist_ok=True)

    # this will organize the file according to the process
    # process is a function which will accept files as an input
    # process should retun a dict which contain the folderName: [files]
    # if you wish to create nested folders give the folder name as path/to/nested/folder - os.path.join will be useful to do platform indipendently
    def organize(self, process):
        files = self.__readLocation()
        output = process(files)
        folders = output.keys()

        self.__createFolders(folders)

        for folder in folders:
            for file in output[folder]:
                self.__moveFile(file, folder)

        
