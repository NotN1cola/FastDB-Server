import os
import json

class Add:
    @staticmethod
    def add(databaseFilePath, goToAddAddress, informationToAdd):
        address_splitted = goToAddAddress.split(".")
        
        # Verifica che il file del database esista
        if os.path.exists(databaseFilePath):
            with open(databaseFilePath, 'r') as file:
                json_content = json.load(file)

            current_level = json_content
            for key in address_splitted[:-1]:
                if key in current_level:
                    current_level = current_level[key]
                else:
                    print(f"Chiave '{key}' non trovata.")
                    return None

            final_key = address_splitted[-1]
            
            # Convertire informationToAdd da stringa a dizionario
            try:
                informationToAdd = json.loads(informationToAdd)
            except json.JSONDecodeError as e:
                print(f"Errore di parsing JSON: {e}")
                return None

            if final_key in current_level and isinstance(current_level[final_key], dict):
                current_level[final_key].update(informationToAdd)
            else:
                print(f"Chiave '{final_key}' non trovata o non è un dizionario.")
                return None

            # Salva le modifiche al file JSON
            with open(databaseFilePath, 'w') as file:
                json.dump(json_content, file, indent=4)

            return json_content

        else:
            print("Il file del database non esiste.")
            return None
