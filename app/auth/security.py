from passlib.context import CryptContext

#Password hashing context configured to use bcrypt
password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

#Hash a plaintext password BEFORE database storage
def hash_password(password: str) -> str:

    return password_context.hash(password)

#Verify a plaintext password against its stored hash
def verify_password(password: str, hashed: str) -> bool:
    
    return password_context.verify(password, hashed)