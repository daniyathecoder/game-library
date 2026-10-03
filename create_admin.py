import getpass 
from database import get_database,init_database
from auth import hash_password
def main():
  init_database()
  print("\\\\YOU DID IT RAMEESHA\\\\")
  print("Game Platfrm admin creator")

  username = input ("Admin username : ").strip()
  password = getpass.getpass("Admin password: ")
  if not username or not password:
    print ("Username and poassword cannot be empty. ")
    return
  connection = get_database()
  existing = connection.execute("SELECT id FROM admins WHERE username = ? ",(username,)).fetchone()
  if existing:
    print("That Username already exists. Try a different username.")
    connection.close()
    return
  password_hash = hash_password(password)
  connection.execute("""INSERT INTO admins (username,password_hash)VALUES(?,?)""",(username,password_hash))
  connection.commit()
  connection.close()
  print()
  print("Admin account created successfully.")
if __name__ == "__main__":
  main()