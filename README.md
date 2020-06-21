[![Documentation Status](https://readthedocs.org/projects/papermerge/badge/?version=latest)](https://papermerge.readthedocs.io/en/latest/?badge=latest)

# Papermerge - Document Management System

Papermerge is an open source document management system (DMS) primarily
designed for archiving and retrieving your digital documents. Instead of
having piles of paper documents all over your desk, office or drawers - you
can quickly scan them and configure your scanner to directly upload to
Papermerge DMS.

Papermerge DMS on its turn will
[OCR](https://en.wikipedia.org/wiki/Optical_character_recognition) the
document and index it. You will be able to quickly find any (scanned!)
document using full text search capabilities.

It is built on Django 3.0.

Papermerge is actively developed.

This is web-based software. This means there is no executable file (aka no
.exe files), and it must be run on a web server and accessed through a web
browser.

## Features
    
* Documents of pdf, jpg, png, tiff formats are supported
* Per page OCR of the documents
* Full Text Search of the scanned documents
* Files and Folders - users can organize documents in folders
* Multi-User
* User permissions management
* Document permissions management
* REST API ([screencast demo](https://vimeo.com/391436134))
* Page Management - delete, reorder, cut & paste pages ([screencast demo](https://www.youtube.com/watch?v=CRhUpPqCI64))

## Resources

 * [Video Demo](https://www.youtube.com/watch?v=U_x8fOhuMTI)
 * [Documentation](https://papermerge.readthedocs.io/)
 * [English Website](https://papermerge.com)
 * [German Website](https://papermerge.de)


## Screenshots

![Screenshot 01](./screenshots/screenshot01.png)
![Screenshot 02](./screenshots/screenshot02.png)
![Screenshot 03](./screenshots/screenshot03.png)

### Try it!

You can try it with just 3 simple commands (you need git and docker-compose):

    git clone git@github.com:ciur/papermerge.git
    cd docker
    docker-compose up -d

Docker compose command will pull all necessary docker images and start
papermerge (stable 1.2 version) on http://localhost:8000. Access it with
default username/password: admin/admin.

### Installation

There are couple options:
    
* [From docker container](https://papermerge.readthedocs.io/en/latest/installation/docker.html)
* [Using systemd](https://papermerge.readthedocs.io/en/latest/installation/systemd.html)
* [Manual way - detailed step by step instructions](https://papermerge.readthedocs.io/en/latest/installation/manual_way.html)
* Deploy it with ansible... coming soon!

### Related Projects

* [MgMail](https://github.com/papermerge/mg-mail) - Imports document attachments from SMTP account/email into Papermerge DMS via REST API key
* [MgClipboard](https://github.com/papermerge/mg-clipboard) - Django Middleware used in Papermerge DMS to power cut/paste of the document/folder/page (IDs) into user's session
* [Django Lessons](https://django-lessons.com) - All knowledge I gain during development of Papermerge nicely presented as screencasts. Screencasts are short and to the point lessons about Django ecosystem


### Contact 

* [Twitter Account](https://twitter.com/papermerge)
* [YouTube Channel](https://www.youtube.com/channel/UC8KjEsDexEERBw_-VyDbWDg)
* [EMail](mailto:eugen@papermerge.com)


