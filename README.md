<h1 align="center">Papermerge DMS</h1>

<p align="center">
<img src="./artwork/logo.png" />
</p>

Papermerge DMS or simply Papermerge is a open source document management
system designed to work with scanned documents (also called digital
archives). It extracts text from your scans using OCR, indexes them, and
prepares them for full text search. Papermerge provides look and feel of
modern desktop file browsers. It has features like dual panel document
browser, drag and drop, tags, hierarchical folders and full text search so
that you can efficiently store and organize your documents.

It supports PDF, TIFF, JPEG and PNG document file formats. Papermerge is
perfect tool for long term storage of your documents.

Papermerge's main use case is **long term storage of digital archives**.

Papermerge DMS is actively developed.

This is web-based software. This means there is no executable file (aka no
.exe files), and it must be run on a web server and accessed through a web
browser.

![Papermerge](./img/papermerge3.png)


## Repositories

**This is meta-repository** - which means that source code of the
application is not here. **This repository is used to track project's existence,
status and its issues.**

As the application grew it was necessary to split it
into multiple repositories and in same time move new repositories under
[Papermerge Github Organization](https://github.com/papermerge).

| Repository      | Description |
| :---------------|-------------|
| [ciur/papermerge](https://github.com/ciur/papermerge)| Meta-repository which keeps track the project existence, status, and its issues.|
| [papermerge/papermerge-core](https://github.com/papermerge/papermerge-core)| Source code for REST API Backend server. The heart of the project.|
| [papermerge/papermerge.js](https://github.com/papermerge/papermerge.js)| Source code for Frontend - desktop like modern user interface.|
| [papermerge/documentation](https://github.com/papermerge/documentation)| Source code for the documentation.|
| [papermerge/openapi-schema](https://github.com/papermerge/openapi-schema)| OpenAPI schema.|
| [papermerge/rest-api-clients](https://github.com/papermerge/rest-api-clients)| Clients generated from OpenAPI schema.|
| [papermerge/papermerge-cli](https://github.com/papermerge/papermerge-cli)| Command line utility to interact with your Papermerge DMS instance (e.g. import recursively local folders).|
| [papermerge/helm-chart](https://github.com/papermerge/helm-chart)| Helm Chart for deploying Papermerge in Kubernetes cluster.|

## Other Resources

| Repository      | Description |
|-----------------|-------------|
|[docs.papermerge.io](https://docs.papermerge.io/)| Online Documentation |
|[REST API reference/swagger](https://docs.papermerge.io/swagger-ui/)| Online REST API reference with swagger UI |
|[REST API reference/redoc](https://docs.papermerge.io/redoc/)| Online REST API reference with redoc UI |
|[https://papermerge.com](https://papermerge.com) | Homepage |
|[YouTube Channel](https://www.youtube.com/channel/UC8KjEsDexEERBw_-VyDbWDg) | YouTube channel |
|[Twitter](https://twitter.com/papermerge) | Twitter |
|[Reddit](https://www.reddit.com/r/Papermerge/) | Reddit |


## Right Tool For You?

To be efficient you always need to choose right tool for the problem. Because
*Document Management* term is too wide - I think that a definition of what is a
*Document* in context of Papermerge software is needed.

For Papermerge a document is anything which is a good candidate for
archiving - some piece of information which is not editable but you need to
store it for future reference. For example receipts are good examples -
you don't need to read receipts everyday, but eventually you will need them
for your tax declaration. In this sense - scanned documents, which are
usually in PDF or TIFF format, are perfect match.

Within Papermerge context terms **document**, **scanned document**, **pdf document**,
and **digital archive** are used interchangeable and mean the same thing.

Papermerge shines when it comes to storing documents for long term, in other words
Papermerge's main use case is **long term storage of digital archives**.

Out of scope are Office documents (ODT, DOCX....), text files (notes) which
usually are editable.

Papermerge is simply not designed to store books. Yes, you can scan a book and
import it in Papermerge, but again - this is not what Papermerge was intended for.

## Features Highlight

* Documents of pdf, jpg, png, tiff formats are supported
* Desktop like user interface
* **OCR** - used to extract text for documents indexing
* Full text search
* Document Versioning (all operations on the documents are non destructive)
* User defined metadata per folder/document/page
* Tags - assign colored tags to documents or folders
* Documents and Folders - users can organize documents in folders
* Multi-User (Groups, Roles)
* User permissions management
* Document permissions management
* REST API
* Page Management - delete, reorder, rotate and extract pages
* Basic automation

See last section for details on feature set in Papermerge 2.0 and Papermerge 2.1

## Donations, Fundraising, Your Support

For donations, you can use PayPal and GitHub Sponsorship:

* [Donate via Paypal](https://www.paypal.com/paypalme/eugenciur)
* [Sponsor via Github](https://github.com/sponsors/ciur)

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


## Papermerge 2.1 Vs Papermerge 2.0

In general rewriting application from scratch is dubious adventure. However,
because Papermerge 2.0 had too many design flaws - maintenance of which, in
short and long term is a serious pain - we've decided, for good or ill, to
rewrite it.

As result Papermerge 2.1 was born. Although they look
similar, **Papermerge 2.0 and Papermerge 2.1 are entirely different and
incompatible applications**.

Because rewriting of Papermerge took by far more time than planned, many
of the 2.0 features still did not made it to Papermerge 2.1. Keep in mind,
that in long term, almost all features of Papermerge 2.0 will be "ported
back" to subsequent versions (e.g. Automates, Metadata).

Here is a table of features comparisons of both versions:

| Feature      | Papermerge 2.0 | Papermerge 2.1 | Remarks |
|-----------------|-------------|----------------|----------------------|
|PDF format| :heavy_check_mark: |:heavy_check_mark:| |
|png format| :heavy_check_mark: |:x:| Will be ported in future versions|
|jpeg format| :heavy_check_mark: |:x:| Will be ported in future versions|
|tiff format| :heavy_check_mark: |:x:| Depending on request, may be ported in future versions|
|Desktop like UI|:heavy_check_mark:|:heavy_check_mark:| in 2.1 UI is reactive|
|Dual Panel|:x:|:heavy_check_mark:||
|Realtime OCR feedback|:x:|:heavy_check_mark:||
|OCR|:heavy_check_mark:|:heavy_check_mark:| in 2.1 uses [OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/)|
|Download document with OCRed text layer|:x:|:heavy_check_mark:| in 2.1 uses [OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/)|
|Full Text Search|:heavy_check_mark:|:heavy_check_mark:|in 2.1 you can choose between multiple search backends|
|Document Versioning|:x:|:heavy_check_mark:|Actually 2.0 has some very limited and hacky support for document versions|
|User defined metadata per folder/document/page|:heavy_check_mark:|:x:|Will be ported in future versions|
|Automates|:heavy_check_mark:|:x:|Will be ported in future versions|
|Tags - assign colored tags to documents or folders|:heavy_check_mark:|:heavy_check_mark:||
|Documents and Folders|:heavy_check_mark:|:heavy_check_mark:||
|Multi-User (Groups, Roles)|:heavy_check_mark:|:heavy_check_mark:||
|User permissions management|:heavy_check_mark:|:heavy_check_mark:||
|Document permissions management|:heavy_check_mark:|:x:|Will be ported in future versions|
|REST API|:heavy_check_mark:|:heavy_check_mark:||
|Page Delete/Reorder/Move|:heavy_check_mark:|:heavy_check_mark:||
|Page Rotation|:x:|:heavy_check_mark:||
|Documents Merging|:x:|:heavy_check_mark:||
|Cloud Native/K8s Support|:x:|:heavy_check_mark:||
