.. _automation:

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

.. caution::
  
   It is crucial to understand that **matching is per Page**. Thus, statement *match a document* is not entirely correct. 
   Automation processes is triggered every time when OCR for certain page completes. OCRed page is sent to automation module and Papermerge will try to match each automate instance on it. In case there is a match - it is considered that document matched automate criteria, although technically correct is - page of respective the document matched!

There are 4 different ways to match:

1. Any
2. All
3. Literal
4. Regular Expression

With ``Any`` matching algorithm, document matches **if any of mentioned keyword will match**.
With ``All``, document matches **if all mentioned keywords are found in document**. Keywords order does not matter.
With ``Literal``, match means that the text you enter must appear in the document exactly as you've entered it.
You can use ``Regular Expression`` for matching criteria. Regular expressions is a general programming method of text matching. Computer programmers usually know what it means.  

Move to Destination Folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~


Extract Metadata and Meta-Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Extract Page
~~~~~~~~~~~~~