from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='ldap-iitmandi',
    version='1.0',
    author="Abhi Nandan",
    author_email="nandan645@protonmail.com",
    description="Quick login into the annoying LDAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nandan645/LDAP-Auto-Login",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
	    'ldap-login=ldaplogin.login:ldap_login',
            'ldap-logout=ldaplogin.logout:ldap_logout',
            'ldap-setup=ldaplogin.setup_credentials:setup_credentials',
        ],
    },
    install_requires=[
        # List your package dependencies here
        'httpx',
        'beautifulsoup4',
        'keyring',
    ],

)
