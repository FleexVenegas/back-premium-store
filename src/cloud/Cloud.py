import cloudinary
from decouple import config

class CloudConfig:

    @classmethod
    def get_connection_cloud(self):
        try:
            return cloudinary.config(   
                cloud_name = config('CLOUD_NAME'),
                api_key = config('API_KEY'),
                api_secret = config('API_SECRET')
            )
        except Exception as ex:
            return str(ex)
        
    