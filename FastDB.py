import json
import sys
from colorama import Fore
from threading import Thread
import os
import socket
import platform
from events.logSystem import logSystem
from events.loginSystem import authenticationSystem
from events.addlocalAdmin import addlocalAdmin
from commands.getAll import getAll
from commands.getByAddress import getByAddress
from commands.createDatabase import createDatabase
from commands.add import Add

local_directory = os.path.dirname(os.path.realpath(__file__))
databases_directory = os.path.join(local_directory, 'databases')
loginsFile = os.path.join(local_directory, 'events', 'logins', 'logins.json')
logs_directory = os.path.join(local_directory, "logs")

def clearCMD():
    if platform.system() == 'Windows':
        return os.system("cls")
    elif platform.system() == 'Linux':
        return os.system("clear")

class DatabaseHandler:
    @staticmethod
    def handle_database(database, action, rawCommand):
        local_directory = os.path.dirname(os.path.realpath(__file__))
        databases_directory = os.path.join(local_directory, 'databases')
        rawCommandSplited = rawCommand.split()

        db_path = os.path.join(databases_directory, f"{database}.json")
        
        if action == 'getall':
            if len(rawCommandSplited) < 3:
                print("Invalid command format. Token missing.")
                logSystem.addInfo(logsFile, "Invalid command format. Token missing.")
                return None
            
            token = rawCommandSplited[2]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")
            logSystem.addInfo(logsFile, f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                logSystem.addInfo(logsFile, f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all' or permsSplited[0] == database:
                    if permsSplited[1] == "superAdmin" or permsSplited[1] == "localAdmin":
                        print(f"Fetching all data from database {database}...")
                        logSystem.addInfo(logsFile, f"Fetching all data from database {database}...")
                        return getAll.getAll(db_path)
            print("User does not have permission or invalid token provided.")
            logSystem.addInfo(logsFile, "User does not have permission or invalid token provided.")
            return None
        
        elif action == 'getbyaddress':
            if len(rawCommandSplited) < 4:
                print("Invalid command format. Address or token missing.")
                logSystem.addInfo(logsFile, "Invalid command format. Address or token missing.")
                return None
            
            address = rawCommandSplited[2]
            token = rawCommandSplited[3]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")
            logSystem.addInfo(logsFile, f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                logSystem.addInfo(logsFile, f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all' or permsSplited[0] == database:
                    if permsSplited[1] == "superAdmin" or permsSplited[1] == "localAdmin":
                        print(f"Fetching data by address from database {database}...")
                        logSystem.addInfo(logsFile, f"Fetching data by address from database {database}...")
                        return getByAddress.getByAddress(db_path, address)
            print("User does not have permission or invalid token provided.")
            logSystem.addInfo(logsFile, "User does not have permission or invalid token provided.")
            return None
        
        elif action == 'createdatabase':
            if len(rawCommandSplited) < 3:
                print("Invalid command format. Database name or token missing.")
                logSystem.addInfo(logsFile, "Invalid command format. Database name or token missing.")
                return None
            
            databaseName = rawCommandSplited[1]
            token = rawCommandSplited[2]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")
            logSystem.addInfo(logsFile, f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                logSystem.addInfo(logsFile, f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[1] == "superAdmin":
                    print(f"Creating a new database named {databaseName}...")
                    logSystem.addInfo(logsFile, f"Creating a new database named {databaseName}...")
                    createDB = createDatabase.createDatabase(databases_directory, databaseName)

                    if createDB == True:
                        return "File created successfully!"
                    else:
                        return "File already exists, try with another name."
                            
            print("User does not have permission or invalid token provided.")
            logSystem.addInfo(logsFile, "User does not have permission or invalid token provided.")
            return None
        
        elif action == 'add':
            if len(rawCommandSplited) < 5:
                print("Invalid command format. Address or token missing.")
                logSystem.addInfo(logsFile, "Invalid command format. Address or token missing.")
                return None
            
            address = rawCommandSplited[2]
            infoToAdd = ' '.join(rawCommandSplited[3:-1])
            token = rawCommandSplited[-1]

            try:
                json.loads(infoToAdd)
            except json.JSONDecodeError as e:
                print(f"Errore di parsing JSON: {e}")
                logSystem.addInfo(logsFile, f"Errore di parsing JSON: {e}")
                return None

            perms = authenticationSystem.hasUserPermission(token)
            print(f"Permissions: {perms}")
            logSystem.addInfo(logsFile, f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                logSystem.addInfo(logsFile, f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all' or permsSplited[0] == database:
                    if permsSplited[1] == "superAdmin" or permsSplited[1] == "localAdmin":
                        print(f"Adding data to database {database}...")
                        logSystem.addInfo(logsFile, f"Adding data to database {database}...")
                        return Add.add(db_path, address, infoToAdd)
            print("User does not have permission or invalid token provided.")
            logSystem.addInfo(logsFile, "User does not have permission or invalid token provided.")
            return None
        
        elif action == 'addlocaladmin':
            if len(rawCommandSplited) < 3:
                print("Invalid command format. Address or token missing.")
                logSystem.addInfo(logsFile, "Invalid command format. Address or token missing.")
                return None
            
            database = rawCommandSplited[1]
            databaseFile = f"{rawCommandSplited[1]}.json"
            token = rawCommandSplited[2]
            databasePath = os.path.join(databases_directory, databaseFile)

            perms = authenticationSystem.hasUserPermission(token)
            print(f"Permissions: {perms}")
            logSystem.addInfo(logsFile, f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                logSystem.addInfo(logsFile, f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all':
                    if permsSplited[1] == "localAdmin":
                        print(f"Adding localAdmin to logins...")
                        logSystem.addInfo(logsFile, f"Adding localAdmin to logins...")
                        return addlocalAdmin.addlocalAdmin(database, databasePath)
            print("User does not have permission or invalid token provided.")
            logSystem.addInfo(logsFile, "User does not have permission or invalid token provided.")
            return None

        else:
            raise ValueError(f"Unsupported action: {action}")

class RequestHandler:
    @staticmethod
    def handle_request():
        HOST = "127.0.0.1"
        PORT = 5000

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on {HOST}:{PORT}")
            logSystem.addInfo(logsFile, f"Server listening on {HOST}:{PORT}")

            while True:
                conn, addr = s.accept()
                t = Thread(target=RequestHandler.connection, args=(conn, addr))
                t.start()

    @staticmethod
    def connection(conn, addr):
        print(f"Connected by {addr}")
        logSystem.addInfo(logsFile, f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                command = data.decode().strip()
                commandSplited = command.split()
                print(f"Received command: {command}")
                logSystem.addInfo(logsFile, f"Received command: {command}")

                if commandSplited[0].lower() == 'getall':
                    print("Processing 'getall' command...")
                    logSystem.addInfo(logsFile, "Processing 'getall' command...")
                    info = DatabaseHandler.handle_database(f"{commandSplited[1]}", 'getall', command)
                    print(f"Response from 'getall': {info}")
                    logSystem.addInfo(logsFile, f"Response from 'getall': {info}")
                    response = str(info).encode()
                    conn.sendall(response)
                elif commandSplited[0].lower() == 'getbyaddress':
                    print("Processing 'getbyaddress' command...")
                    logSystem.addInfo(logsFile, "Processing 'getbyaddress' command...")
                    info = DatabaseHandler.handle_database(f"{commandSplited[1]}", 'getbyaddress', command)
                    if info is None:
                        response = "Indirizzo non trovato o invalido.".encode()
                    else:
                        print(f"Response from 'getbyaddress': {info}")
                        logSystem.addInfo(logsFile, f"Response from 'getbyaddress': {info}")
                        response = str(info).encode()
                    conn.sendall(response)
                elif commandSplited[0].lower() == 'createdatabase':
                    print("Processing 'createdatabase' command...")
                    logSystem.addInfo(logsFile, "Processing 'createdatabase' command...")
                    info = DatabaseHandler.handle_database(None, 'createdatabase', command)
                    print(f"Response from 'createdatabase': {info}")
                    logSystem.addInfo(logsFile, f"Response from 'createdatabase': {info}")
                    response = str(info).encode()
                    conn.sendall(response)
                elif commandSplited[0].lower() == 'add':
                    print("Processing 'add' command...")
                    logSystem.addInfo(logsFile, "Processing 'add' command...")
                    info_to_add = ' '.join(commandSplited[3:-1])
                    token = commandSplited[-1]

                    try:
                        json_data = json.loads(info_to_add)
                    except json.JSONDecodeError as e:
                        print(f"Errore di parsing JSON: {e}")
                        logSystem.addInfo(logsFile, f"Errore di parsing JSON: {e}")
                        conn.sendall("Errore di parsing JSON: JSON non valido.".encode())
                        return

                    info_to_add_str = json.dumps(json_data)
                    
                    info = DatabaseHandler.handle_database(f"{commandSplited[1]}", 'add', f"{commandSplited[0]} {commandSplited[1]} {commandSplited[2]} {info_to_add_str} {token}")
                    
                    if info is None:
                        response = "Errore durante l'aggiunta delle informazioni al database.".encode()

                    else:
                        print(f"Response from 'add': {info}")
                        logSystem.addInfo(logsFile, f"Response from 'add': {info}")
                        response = str(info).encode()
                    conn.sendall("Data added successfully!".encode())

                elif commandSplited[0].lower() == 'addlocaladmin':
                    dbPath = os.path.join(databases_directory, f"{commandSplited[1]}.json")
                    print("Processing 'addlocaladmin' command...")
                    logSystem.addInfo(logsFile, "Processing 'addlocaladmin' command...")
                    info = addlocalAdmin.addlocalAdmin(commandSplited[1], dbPath, loginsFile)
                    print(f"Response from 'addlocaladmin': {info}")
                    logSystem.addInfo(logsFile, f"Response from 'addlocaladmin': {info}")
                    response = str(info).encode()
                    conn.sendall(response)

                else:
                    print(f"Unknown command: {command}")
                    logSystem.addInfo(logsFile, f"Unknown command: {command}")
                    response = f"Unknown command: {command}".encode()
                    conn.sendall(response)

def print_menu():
    print("""███████╗ █████╗ ███████╗████████╗██████╗ ██████╗ 
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
█████╗  ███████║███████╗   ██║   ██║  ██║██████╔╝
██╔══╝  ██╔══██║╚════██║   ██║   ██║  ██║██╔══██╗
██║     ██║  ██║███████║   ██║   ██████╔╝██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═════╝ ╚═════╝ 
                                                    """)
    logSystem.addInfo(logsFile, "Displaying menu...")

def main():
    clearCMD()
    print_menu()
    
    if not os.path.exists(databases_directory):
        os.makedirs(databases_directory)

    if sys.argv[1] == 'startserver'.lower():
        RequestHandler.handle_request()
    elif sys.argv[1] == 'createsuperadmin'.lower():
        token = authenticationSystem.createToken()

        data_to_add = {
            str(token): ["all", "superAdmin"]
        }
        json_data_to_add = json.dumps(data_to_add)

        result = Add.add(loginsFile, "login", json_data_to_add)
        if result:
            print(f"SuperAdmin creato con successo!" + Fore.RED + f"\nTOKEN: {token}" + Fore.RESET)
            logSystem.addInfo(logsFile, f"SuperAdmin creato con successo! TOKEN: {token}")
        else:
            print("Errore durante la creazione del SuperAdmin.")
            logSystem.addInfo(logsFile, "Errore durante la creazione del SuperAdmin.")

if __name__ == "__main__":
    logsFileSplited = logSystem.createLogFile(logs_directory).split(",")
    logsFile = logsFileSplited[0]

    main()
