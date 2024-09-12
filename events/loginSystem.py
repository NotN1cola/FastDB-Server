import json
import secrets
import os

class authenticationSystem:
    @staticmethod
    def createToken():
        return secrets.token_urlsafe(40)
    
    @staticmethod
    def hasUserPermission(token):
        # Determina il percorso del file logins.json
        local_directory = os.path.dirname(os.path.realpath(__file__))
        logins_directory = os.path.join(local_directory, 'logins')
        loginsFile = os.path.join(logins_directory, 'logins.json')

        print(f"Checking logins file at: {loginsFile}")  # Debug: verifica il percorso del file

        # Verifica se il file logins.json esiste
        if os.path.exists(loginsFile):
            with open(loginsFile, 'r') as file:
                fileContent = file.read()
                print(f"File content: {fileContent}")  # Debug: stampa il contenuto del file

                jsonLoadedFile = json.loads(fileContent)
                
                # Accedi alla sezione "login" del JSON
                login_data = jsonLoadedFile.get("login", {})
                print(f"Login data loaded: {login_data}")  # Debug: stampa i dati di login caricati
                
                # Verifica se il token esiste nei dati di login
                if token in login_data:
                    # Estrai l'informazione associata al token
                    user_info = login_data[token]
                    forDatabase = user_info[0]  # il primo elemento è il nome utente o database a cui ha accesso
                    role = user_info[1]        # il secondo elemento è il ruolo

                    # Restituisce le informazioni del permesso come stringa
                    print(f"Token found. Permissions: {forDatabase}, {role}")  # Debug: stampa i permessi trovati
                    return f"{forDatabase},{role}"
                else:
                    print("Token not found.")  # Debug: il token non è stato trovato
                    return False
        else:
            print(f"Logins file not found at: {loginsFile}")  # Debug: il file non è stato trovato
            return False
