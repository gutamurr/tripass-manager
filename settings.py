import os
import dotenv

dotenv.load_dotenv('.env')
API_KEY = os.environ['API_KEY'] # telegram bot token