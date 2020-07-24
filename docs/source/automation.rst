Automation
============

.. note::

    This is new feature which will be part of 1.4.0 release (available in August 2020). 

With Automation feature you can do 3 things:

1. automatically moving (cut/paste) of documents into their destination folder
2. automatically extract metadata from the document
3. and please forgive me for repetition - automatically extract pages

The whole idea is to remove boring and repetitive tasks.


.. figure:: img/automates/01-automates.png


Each automate instance consists of two very important parts:
    
* matching - what documents it applies to?
* action - what shall it do with matched document? 

Matching
~~~~~~~~~

In order to decide if automate instance applies to current document - it will look for certain
keywords in the document. For example if document contains capital case AWO and number 2020, then this document
must be routed to folder AWO/2020; if document contains word Linode and year 2020, then it will be routed to
Invoices/CloudExpenses/2020.


Move to Destination Folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~


Extract Metadata and Meta-Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Extract Page
~~~~~~~~~~~~~