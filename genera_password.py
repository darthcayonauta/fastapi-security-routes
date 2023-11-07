from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

my_password = input("Ingresa tu password::")
pwd = get_password_hash(my_password)

print(f"Hashed password ===> {pwd}")