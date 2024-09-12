import os
from events.loginSystem import authenticationSystem as aS
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class createDatabase:
    def createDatabase(databasesDirectory, databaseName):
        databaseFileDirectory = os.path.join(databasesDirectory, f"{databaseName}.json")

        if os.path.exists(databaseFileDirectory) == False:
            with open(databaseFileDirectory, 'w') as file:
                file.write("{\n    \n}")
            return True

        else:
            return False