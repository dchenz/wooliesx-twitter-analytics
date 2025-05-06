import dotenv
import os

dotenv.load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "")
