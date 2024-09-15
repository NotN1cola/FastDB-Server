import os
import datetime

class logSystem:
    @staticmethod
    def createLogFile(logs_directory):
        # Ensure the logs directory exists
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)
        
        # Create the log file with a timestamp
        log_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        filePath = os.path.join(logs_directory, log_filename)
        
        # Create the file
        with open(filePath, 'a') as file:
            file.write("Log file created.\n")
        
        return filePath

    def addInfo(logsFile, info):
        with open(logsFile, 'a') as file:
            file.writelines(f"{info}\n")
        return "Info added succesfully!"
