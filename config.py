# Responsible for the internal settings of the application
import os
from dotenv import load_dotenv

load_dotenv()

class Config: 
    MONGO_URI = os.getenv('MONGO_URI')