import os
import bcrypt


HASH_SALT = os.getenv("HASH_SALT")


async def generate_password_hash(password:str) -> str:
    # converting password to array of bytes
    bytes = password.encode('utf-8')
    salt = HASH_SALT.encode('utf-8')
    # generating the salt
    # salt = bcrypt.gensalt()
    
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash

async def check_password_hash(input_password:str) -> bool:

    # converting password to array of bytes
    salt = HASH_SALT.encode('utf-8')
    password_encode = input_password.encode('utf-8')

    # userPassword_encode = hash_Password.encode('utf-8')
    
    result = bcrypt.hashpw(password_encode, salt)
    # result = bcrypt.checkpw(password_encode, salt)
    # generating the salt

    return result


async def set_password(password):
    password_hash = await generate_password_hash(password)
    return password_hash

    user['email'] = str(await check_password_hash(user['email']))
