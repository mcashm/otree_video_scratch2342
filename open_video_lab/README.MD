Installation

python libraries required:

PyJWT
Cryptography

pip install pyjwt
pip install cryptography


open_video_lab needs a RSA SSH Key Pair in PEM format.  See developer.8x8.com/jaas/docs/api-keys-generate-add for details on generation. Do not create a password for the private key.

Save these files into a (hidden, gitignored) subdirectory of the open_video_lab app named .ssh This will create two files in the folder .ssh, a private key file ending in .key and a second key file for the public key in PEM format, ending in .pub 

A (gitnored) python file containing constants that define api keys, app ids, and paths to keys is also necessary.  a sample_jaas_secrets.py file is provided in the repository.  Replace the placeholders with your own keys and rename the file to just jaas_secrets.py

