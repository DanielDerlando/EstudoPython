from passlib.context import CryptContext

pwd_context = CryptContext(schemes="bcrypt",depricated="auto")

def hash(password:str):
    return pwd_context.hash(password)