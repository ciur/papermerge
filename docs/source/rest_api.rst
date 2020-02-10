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
    
    1. get a token
    2. use the token from 3rd party REST API client

Get a Token
~~~~~~~~~~~~~

1. Click User Menu (top right corner) -> API Tokens
2. Click New Token
3. You will to decide on number of hours the token will be valid. Default is 4464 hours, which is roughly equivalent of 6 months. Click *Save* button.
4. After you click *Save* button, two information messages will be displayed. **Write down** your token from *Remember the token: ...* info window.

.. figure:: img/01_token_api_user_menu.png

   "API Tokens" in User Menu (step 1)

.. figure:: img/02_new_token_button.png

   "New token" button (step 2)

.. figure:: img/03_displayed_token.png

    In green color is your token (step 4)


Use the Token
~~~~~~~~~~~~~~~
