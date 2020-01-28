Design
=======

A brief description of the architecture of Papermerge and why such
design decisions were taken. Papermerge project has 2 parts:

    * Web Application
    * Workers

Web application is further devided into Frontend and Backend. As result
there are 3 separate repositories that are part of one whole.

.. image:: img/design1.png

1. Frontend
***********
`Papermerge-js Repository <https://github.com/ciur/papermerge-js>`_

.. warning::
    Name *papermerge-js* is misleading, because it implies that it is only
    javascript is used, which is not true. This project manages all static
    assets: javascript, css, images, fonts.

Modern web applications tend to use a lot of javascript and css. Javascript
code, as opposite to code written in Python, become increasingly difficult to manage.
Same is for css.
To deal with codebase complexity, I decided to split frontend as completely separate 
project. This project is a `Webpack project <https://webpack.js.org/>`_. In practice this
makes it little bit easier to deal with growing javascript code complexity.
The outcome of this project, among others, are two important files:: 
        
        <papermerge-js>/static/js/papermerge.js
        <papermerge-js>/static/css/papermerge.css

There are static files as well, like images and fonts. However images and fonts, are just
placed in ``<papermerge-js>/static`` and nothing really interesting happens with them.

2. Backend
**********

`Papermerge-proj Repository <https://github.com/ciur/papermerge>`_

Backend is a `Django <https://djangoproject.com>`_ application.


3. Wrokers
***********
`Papermerge-worker Repository <https://github.com/ciur/papermerge-worker>`_
