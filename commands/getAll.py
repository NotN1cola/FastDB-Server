import os

class getAll:
    def getAll(file_path):
        if os.path.exists(file_path) == True:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
    
        else:
            return "Database not found."