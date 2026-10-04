import os
from dotenv import load_dotenv

load_dotenv()

# os.getenv() -> it returns None if find nothing that could pass on and our app would move in to other errors
JWT_SUPER_KEY = os.environ["jwt_secret_key"] # raises an error and app stops if it not find the super key in env