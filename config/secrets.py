from os import environ
from dotenv import load_dotenv


load_dotenv()

# Application
APP_SECRET = environ['APP_SECRET']
JWT_SECRET = environ['JWT_SECRET']


# Database
MONGO_URI = environ['MONGO_URI']
