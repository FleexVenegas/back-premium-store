from flask import json

class Tools:
    
    @classmethod
    def convert_json(self, _string):
        # Convertir la string en formato JSON
        _dict = json.loads(_string)

        return _dict
    

    