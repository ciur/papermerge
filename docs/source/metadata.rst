Metadata
============

.. warning::

	Metadata is a new feature introduced since  version 1.3.0 and it will be available since July 2020.

Main Concepts
~~~~~~~~~~~~~~

Metadata is extra information about your documents. In other words - data about your data.
Following picture is a (scanned document) receipt with highlighted shop name, price and date on it.

.. figure:: img/metadata/01-macgeiz-receipt-with-metadata.png

   Receipt with metadata

This additional information - shop name, price and date is so called document's **metadata**.
Metadata is extremely useful when you need to *locate specific document among many other very similar documents*.

Imagine that you scanned 60 groceries receipts and *organized* them in a folder named Groceries.
If would just store those receipts on an ordinary file system the only way to distinguish between files
is by file names or maybe by their text search if your storage supports OCR. Finding, specific file, say the receipts you got in June 2020, would be time consuming.

A more efficient and practical way to tackle this problem is by associating to
all scanned documents (receipts in this example) - metadata. Let's continue
with groceries receipts example. It would very time consuming to go to each
document and add metadata to each file individually. A faster way to create metadata and
associated it to any file, is by simple creating a folder - add metadata to
that folder - let's name it Groceries-2020 - and then just copy all groceries
related files into that folder.

.. figure:: img/metadata/02-inherited-metadata.png

   Metadata is inherited from folder to all documents within it