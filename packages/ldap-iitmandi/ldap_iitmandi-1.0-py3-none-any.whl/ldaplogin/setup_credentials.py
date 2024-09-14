import keyring

def setup_credentials():
    import getpass
    username = input("Enter your LDAP username: ")
    password = getpass.getpass("Enter your LDAP password: ")
    # Store the credentials in the keyring
    keyring.set_password("ldaplogin", "username", username)
    keyring.set_password("ldaplogin", "password", password)
    print("Credentials have been securely stored.")
