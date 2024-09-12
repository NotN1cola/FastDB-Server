import json
import os

class getByAddress:
    @staticmethod
    def getByAddress(file_path, address):
        address_splitted = address.split(".")

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                json_content = json.loads(content)

                current_level = json_content
                for key in address_splitted:
                    if key in current_level:
                        print(f"Trovata chiave '{key}' nel livello corrente: {current_level[key]}")
                        current_level = current_level[key]
                    else:
                        print(f"Chiave '{key}' non trovata.")
                        return None
                
                return current_level
        else:
            print("Il file non esiste.")
            return None
