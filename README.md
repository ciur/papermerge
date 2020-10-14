[![Documentation Status](https://readthedocs.org/projects/papermerge/badge/?version=latest)](https://papermerge.readthedocs.io/en/latest/?badge=latest)
[![Travis](https://travis-ci.com/ciur/papermerge.svg?branch=master)](https://travis-ci.com/github/ciur/papermerge)
[![Docker Pulls](https://img.shields.io/docker/pulls/eugenci/papermerge)](https://hub.docker.com/r/eugenci/papermerge)
[![Contributors](https://img.shields.io/badge/-Contributors-important)](https://github.com/ciur/papermerge/blob/master/CONTRIBUTORS.md)

![Papermerge](./artwork/logo.png)

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

It is built on [Django 3.0](https://www.djangoproject.com/).

Papermerge is actively developed and I [release quite frequently](https://github.com/ciur/papermerge/releases).

This is web-based software. This means there is no executable file (aka no
.exe files), and it must be run on a web server and accessed through a web
browser.

## Right Tool For You?

To be efficient you always need to choose right tool for the problem. Because
*Document Management* is too generic - I think that a definition of what is a
*Document* in context of this software is needed.

For Papermerge a document is anything which is a good candidate for archiving - some piece of information which is not editable but you need to store it for
future reference. For example receipts are perfect examples - you don't need to
read receipts everyday, but eventually you will need them for your tax
declaration. In this sense - scanned documents, which are usually
in PDF or TIFF format, are perfect match.

Out of scope (at least for near future) are Office documents (ODT, DOCX....),
text files (notes) which usually are editable. In future Papermerge might support Office documents (ODT etc), but that feature will be provided as plugins.

Papermerge is simply not designed to store books. Yes, you can scan a book and import it in Papermege, but again - this is not what Papermerge was designed for.

## Features
    
* Documents of pdf, jpg, png, tiff formats are supported
* Per page OCR of the documents
* Full Text Search of the scanned documents
* Tags - assign colored tags to documents or folders ([screencast demo](https://www.youtube.com/watch?v=bshUowL57t8))
* Documents and Folders - users can organize documents in folders
* Multi-User
* User permissions management
* Document permissions management
* REST API ([screencast demo](https://vimeo.com/391436134))
* Page Management - delete, reorder, cut & paste pages ([screencast demo](https://www.youtube.com/watch?v=CRhUpPqCI64))
* Basic automation ([screencast demo](https://www.youtube.com/watch?v=5adbHHmNcEw))

## Live Demo

In live demo some of the features are disabled. For example you cannot manage
users, API tokens. Folders/documents with a red lock are read-only for guest user.

* [Live demo](https://demo.papermerge.com)
* Username: ``guest``
* Password: ``password77a``


## Documentation and Other Resources

Papermerge has high quality, up-to-date and to the point
[documentation](https://papermerge.readthedocs.io/). Documentation contains
lots of images, text and videos. It is regularly updated. If you spot
outdated or incomplete article please open an issue on github - it will
be handled immediately. Documentation issues have high priority.

 * [Documentation URL](https://papermerge.readthedocs.io/)
 * [Video Demo](https://www.youtube.com/watch?v=OpwTaEN5t2Y)
 * [English Website](https://papermerge.com)
 * [German Website](https://papermerge.de)

## Contributing

We welcome contributions! In general, if change is very small, like fixing a
documentation typo, remove unused variable or minor adjustments of docker
related files - you can create a pull request right away. If your change is
small and reasonable it will be (very likely) almost immediately accepted. 

For bigger changes, like a new feature or even change/add/remove of
whole paragraph in documentation - please **first discuss the
change** you wish to make via GitHub issue, pull request or [email](mailto:eugen@papermerge.com).

For more information, see the
[contributing](https://github.com/ciur/papermerge/blob/master/CONTRIBUTING.md)
file.

## Screenshots

![Screenshot 01](./screenshots/screenshot-1.png)
![Screenshot 02](./screenshots/screenshot-2.png)
![Screenshot 03](./screenshots/screenshot-3.png)

### Try it!

You can try it with just 3 simple commands (you need git and docker-compose):

    git clone git@github.com:ciur/papermerge.git
    cd docker/1.4/
    docker-compose up

Docker compose command will pull all necessary docker images and start
papermerge (stable 1.4.0 version) on http://localhost:8000. Access it with
default username/password: admin/admin.

### Installation

There are couple options:
    
* [From docker container](https://papermerge.readthedocs.io/en/latest/setup/docker.html)
* [Using systemd](https://papermerge.readthedocs.io/en/latest/setup/systemd.html)
* [Manual way - detailed step by step instructions](https://papermerge.readthedocs.io/en/latest/setup/manual_way.html)

### Comparison With Other DMS

From my own reasearch I found another two very similar projects - [Paperless](https://github.com/the-paperless-project/paperless) and [MayanEDMS](https://www.mayan-edms.com/). Similar to the way parents tend to love their own children more - I am biased towards my own project - Papermerge. So, below is a comparison table of the three based on my research.

|  Metric  | Papermerge | [MayanEDMS](https://www.mayan-edms.com/) | [Paperless](https://github.com/the-paperless-project/paperless)         
|----------|:-----------:|:---------------------------------------:|:---------------:|
|OCR   | Yes | Yes | Yes |
|Metadata |  Yes | Yes | No |
|Folders/Cabinets| Yes (Folders) | Yes (Cabinets) | No |
|Advanced Permissions Management | Yes | Yes | No |
|Documents Versioning| No | Yes | No | 
|Digital Signatures | No | Yes | No |
|Workflows| Partial (Automation) | Yes | No |
|Tags     | Yes | Yes | Yes |
|REST API | Yes | Yes | Yes |
|License  | Apache-2.0 | Apache 2.0 | GPLv3 |
|Status| Active Development | Active Development | Maintenance / No Development| 
|Initial Release| February 9, 2020 | February 3, 2011 | ~ 2015 |
|Python3?| Yes | Yes | Yes|

### Contact 

For feedback, questions and suggestions send me an
[email](mailto:eugen@papermerge.com). I speak both - German and English, so
you can write me in whatever language you feel more confortable with.

* [EMail](mailto:eugen@papermerge.com)
* [Twitter Account](https://twitter.com/papermerge)
* [YouTube Channel](https://www.youtube.com/channel/UC8KjEsDexEERBw_-VyDbWDg)

