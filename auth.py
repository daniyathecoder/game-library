import hashlib
import hmac
import secrets
from fastapi import HTTPException,Request
def hash_password(password : str)-> str:
   salt = secrets.token_bytes(16)
   password_hash = hashlib.scrypt(password.encode("utf-8"),
                                  salt =salt,n=2**14,r=8,p=1)
   return (salt.hex()+":"+password_hash.hex())

def verify_password(password:str,stored_hash:str)->bool:
   try:
      salt_hex,hash_hex = stored_hash.split(":")
      salt = bytes.fromhex(salt_hex)
      expected_hash  =bytes.fromhex(hash_hex)
      actual_hash = hashlib.scrypt(password.encode("utf-8"),salt=salt,n = 2**14,r=8,p=1)
      return hmac.compare_digest(actual_hash,expected_hash)
   except Exception:
      return False

def require_admin(request:Request):
   admin_id = request.session.get("admin_id")
   if not admin_id:
      raise HTTPException(status_code = 401,detail="Admin authentication required")
   return admin_id
   