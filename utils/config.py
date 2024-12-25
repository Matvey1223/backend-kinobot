from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
POSTGRES_URL = os.getenv('POSTGRES_URL')