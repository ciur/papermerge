REST API
=========

REST API is a way to interact with Papermerge far beyond Web Browser realm.
It gives you power to extend Papermerge in many interesting ways.
For example it allows you to write a simple bash script to automate uploading
of files from your local (or remote) computer's specific location.

Another practical scenario where REST API can be used is to automatically
(well, you need some sort of 3rd party script for that)
import attached documents from a given email account.

How It Works?
**************

Instead of usual Sign In, with username and password, via Web Browser,
you will *sign in* with a token (a fancy name for sequence of numbers and letters)
from practically any software which supports http protocol.

Thus, working with REST API is two step process:
    
    1. get the token
    2. use token from 3rd party REST API client


Get The Token
~~~~~~~~~~~~~~~

1. Click User Menu (top right corner) -> API Tokens
2. Click New Token