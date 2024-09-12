from threading import Thread
import os
import socket
import platform
from commands.getAll import getAll
from commands.getByAddress import getByAddress
from events.loginSystem import authenticationSystem
from commands.createDatabase import createDatabase
from commands.add import Add

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

        # Determina il percorso del database
        db_path = os.path.join(databases_directory, f"{database}.json")
        
        # Gestione dell'azione 'getall'
        if action == 'getall':
            if len(rawCommandSplited) < 3:
                print("Invalid command format. Token missing.")
                return None
            
            token = rawCommandSplited[2]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all' or permsSplited[0] == database:
                    if permsSplited[1] == "superAdmin" or permsSplited[1] == "localAdmin":
                        print(f"Fetching all data from database {database}...")
                        return getAll.getAll(db_path)
            print("User does not have permission or invalid token provided.")
            return None
        
        # Gestione dell'azione 'getbyaddress'
        elif action == 'getbyaddress':
            # Assicurarsi che ci sia l'indirizzo e il token nel comando
            if len(rawCommandSplited) < 4:
                print("Invalid command format. Address or token missing.")
                return None
            
            address = rawCommandSplited[2]
            token = rawCommandSplited[3]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all' or permsSplited[0] == database:
                    if permsSplited[1] == "superAdmin" or permsSplited[1] == "localAdmin":
                        print(f"Fetching data by address from database {database}...")
                        return getByAddress.getByAddress(db_path, address)
            print("User does not have permission or invalid token provided.")
            return None
        
        elif action == 'createdatabase':
            if len(rawCommandSplited) < 3:
                print("Invalid command format. Address or token missing.")
                return None
            
            databaseName = rawCommandSplited[1]
            token = rawCommandSplited[2]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[1] == "superAdmin":
                    print(f"Creating a new database named {database}...")
                    createDB = createDatabase.createDatabase(databases_directory, databaseName)

                    if createDB == True:
                        return "File created succesfully!"
                    else:
                        return "File already existing, try with an another name."
                    
            print("User does not have permission or invalid token provided.")
            return None
        
        elif action == 'add':
            if len(rawCommandSplited) < 5:
                print("Invalid command format. Address or token missing.")
                return None
            
            address = rawCommandSplited[2]
            infoToAdd = rawCommandSplited[3]
            token = rawCommandSplited[4]
            perms = authenticationSystem.hasUserPermission(token)

            print(f"Permissions: {perms}")

            if perms:
                permsSplited = perms.split(',')
                print(f"Database: {permsSplited[0]}, Role: {permsSplited[1]}")
                if permsSplited[0] == 'all' or permsSplited[0] == database:
                    if permsSplited[1] == "superAdmin" or permsSplited[1] == "localAdmin":
                        print(f"Fetching data by address from database {database}...")
                        return Add.add(db_path, address, infoToAdd)
            print("User does not have permission or invalid token provided.")
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

            while True:
                conn, addr = s.accept()
                t = Thread(target=RequestHandler.connection, args=(conn, addr))
                t.start()

    @staticmethod
    def connection(conn, addr):
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                command = data.decode().strip()
                commandSplited = command.split()
                print(f"Received command: {command}")

                if commandSplited[0].lower() == 'getall':
                    print("Processing 'getall' command...")
                    info = DatabaseHandler.handle_database(f"{commandSplited[1]}", 'getall', command)
                    print(f"Response from 'getall': {info}")
                    response = str(info).encode()
                    conn.sendall(response)
                elif commandSplited[0].lower() == 'getbyaddress':
                    print("Processing 'getbyaddress' command...")
                    info = DatabaseHandler.handle_database(f"{commandSplited[1]}", 'getbyaddress', command)
                    if info is None:
                        response = "Indirizzo non trovato o invalido.".encode()
                    else:
                        print(f"Response from 'getbyaddress': {info}")
                        response = str(info).encode()
                    conn.sendall(response)
                elif commandSplited[0].lower() == 'createdatabase':
                    print("Processing 'createdatabase' command...")
                    info = DatabaseHandler.handle_database(None, 'createdatabase', command)
                    print(f"Response from 'createdatabase': {info}")
                    response = str(info).encode()
                    conn.sendall(response)
                elif commandSplited[0].lower() == 'add':
                    print("Processing 'add' command...")
                    # Unisci tutte le parti successive all'indirizzo per trattare gli spazi nel JSON
                    info_to_add = ' '.join(commandSplited[3:-1])
                    token = commandSplited[-1]
                    info = DatabaseHandler.handle_database(f"{commandSplited[1]}", 'add', f"{commandSplited[0]} {commandSplited[1]} {commandSplited[2]} {info_to_add} {token}")
                    if info is None:
                        response = "Errore durante l'aggiunta delle informazioni al database.".encode()
                    else:
                        print(f"Response from 'add': {info}")
                        response = str(info).encode()
                    conn.sendall("Data added succesfully!".encode())

                else:
                    print(f"Unknown command: {command}")
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
    print(" ")

def main():
    clearCMD()
    print_menu()
    local_directory = os.path.dirname(os.path.realpath(__file__))
    databases_directory = os.path.join(local_directory, 'databases')

    if not os.path.exists(databases_directory):
        os.makedirs(databases_directory)

    RequestHandler.handle_request()

if __name__ == "__main__":
    main()
