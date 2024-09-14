
# ldaplogin-iitmandi

`ldaplogin-iitmandi` is a Python package designed to automate the login and logout process to the IIT Mandi network. It securely stores LDAP credentials using the `keyring` library and provides command-line tools for logging in, logging out, and managing credentials.

## Features
- **Secure Credentials**: Store LDAP credentials in the system's keyring.
- **Automated Login**: Log into the IIT Mandi portal with stored credentials.
- **Automated Logout**: Easily log out of the IIT Mandi portal.
- **Command-line Interface**: Simple commands for setup, login, and logout.

## Installation

Install the package via pip:

```bash
pip install ldap-iitmandi
```

## Setup and Usage

1. **Store Credentials**  
   To securely store your LDAP username and password, run the following command:

   ```bash
   ldap-setup
   ```

2. **Login to the Portal**  
   Once the credentials are set up, you can log in to the IIT Mandi portal using:

   ```bash
   ldap-login
   ```

3. **Logout from the Portal**  
   To log out from the portal:

   ```bash
   ldap-logout
   ```

## Requirements

The package requires the following Python libraries:
- `httpx`
- `beautifulsoup4`
- `keyring`

These are automatically installed with the package.

## License

This package is licensed under the MIT License.

---

This summary provides users with clear instructions to set up and use the `ldaplogin-iitmandi` package for their login and logout automation.
