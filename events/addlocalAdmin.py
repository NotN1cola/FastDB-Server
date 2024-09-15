import json
import sys
import os
from colorama import Fore

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from loginSystem import authenticationSystem as aS
from logSystem import logSystem
from commands.add import Add

local_directory = os.path.dirname(os.path.realpath(__file__))
logins_directory = os.path.join(local_directory, 'events', 'logins', 'logins.json')
logs_directory = os.path.join(local_directory, "logs")
logsFileSplited = logSystem.createLogFile(logs_directory).split(",")
logsFile = logsFileSplited[0]

class addlocalAdmin:
    @staticmethod
    def addlocalAdmin(db, dbPath, loginFilePath):
        # Check if the database file exists
        if not os.path.exists(dbPath):
            print("Il file del database non esiste.")
            logSystem.addInfo(logsFile, "Il file del database non esiste.")
            return f"Errore durante la creazione del localAdmin: Il file del database non esiste. {dbPath}"
        
        token = aS.createToken()
        data_to_add = {
            str(token): [db, "localAdmin"]
        }
        json_data_to_add = json.dumps(data_to_add)

        result = Add.add(loginFilePath, "login", json_data_to_add)
        if result:
            print(f"localAdmin creato con successo!" + Fore.RED + f"\nTOKEN: {token}" + Fore.RESET)
            logSystem.addInfo(logsFile, f"localAdmin creato con successo! TOKEN: {token}")
            return f"localAdmin creato con successo! TOKEN:{token}"
        else:
            print("Errore durante la creazione del localAdmin.")
            logSystem.addInfo(logsFile, "Errore durante la creazione del localAdmin.")
            return "Errore durante la creazione del localAdmin."
