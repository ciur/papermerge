.. _dev_lang_support:

Language Support
*******************

By default, papermerge is hardcoded to work with documents in only two languages -
German and English. Theoretically it can support more than 100 languages.
However, I, as developer and user of this software, included in papermerge only what was
usefull for me (German and English).

You can contribute to this project by adding support (and testing it) for you own language.
It is extremely rewarding experience, because:

    * it is fun
    * you will learn a lot
    * you will create something useful for you and others


What is Language Support?
==========================

There are two parts to consider:

    * User Interface language (text like username, Log out)
    * Document Content (actual content of your documents)



User Interface Language
========================

User Interface language is text you user sees and interacts with. Say labels
for username in German will be Benutzername, or text for Log out in German is
Abmelden. To localize user interface (UI) in your own language you need be
familiar with  `Django way
<https://docs.djangoproject.com/en/3.0/topics/i18n/>`_. It is because main web
application is Django project. 

Contributing to the project in this sense means basically creating/updating file papermerge/<langcode>/LC_MESSAGES/django.po file.


Document Content Language
==========================