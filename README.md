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
| [papermerge/documentation](https://github.com/papermerge/documentation)| Source code for the documentation.|
| [papermerge/ansible](https://github.com/papermerge/ansible)| Ansible playbook for deployment on remote server/VM|

## Other Resources

| Resource        | Description |
|-----------------|-------------|
|[https://docs.papermerge.io](https://docs.papermerge.io/)| Online Documentation |
|[https://papermerge.com](https://papermerge.com) | Homepage |
|[https://papermerge.blog](https://papermerge.blog) | Blog |
|[YouTube Channel](https://www.youtube.com/channel/UC8KjEsDexEERBw_-VyDbWDg) | YouTube channel |
|[X/Former Twitter](https://twitter.com/papermerge) | X/Former Twitter |
|[Reddit](https://www.reddit.com/r/Papermerge/) | Reddit |

## Features Highlight

* Documents of PDF, JPG, PNG, TIFF formats are supported
* Desktop like user interface
* **OCR** - used to extract text for documents indexing
* Full text search
* Document Versioning (all operations on the documents are non destructive)
* Tags - assign colored tags to documents or folders
* Documents and Folders - users can organize documents in folders
* Multi-User
* REST API

See last section for details on feature set in Papermerge 2.0, 2.1, 3.0

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


## Versions 2.0 / 2.1 / 3.0

Papermerge version 2.0, version 2.1 and version 3.0 are entirely different and
incompatible applications.

Here is a table of features comparisons of all three major versions:

| Feature      | 2.0 | 2.1 | 3.0 |
|-----------------|-------------|----------------|----------------------|
|PDF format| :heavy_check_mark: |:heavy_check_mark:|:heavy_check_mark: |
|png format| :heavy_check_mark: |:x:| :heavy_check_mark:|
|jpeg format| :heavy_check_mark: |:x:| :heavy_check_mark:|
|tiff format| :heavy_check_mark: |:x:| :heavy_check_mark:|
|Desktop like UI|:heavy_check_mark:|:heavy_check_mark:| :heavy_check_mark:|
|Dual Panel|:x:|:heavy_check_mark:|:heavy_check_mark:|
|Realtime OCR feedback|:x:|:heavy_check_mark:|:heavy_check_mark:|
|OCR|:heavy_check_mark:|:heavy_check_mark:| :heavy_check_mark:|
|Download document with OCRed text layer|:x:|:heavy_check_mark:| :heavy_check_mark:|
|Full Text Search|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|Document Versioning|:x:|:heavy_check_mark:|:heavy_check_mark:|
|User defined metadata per folder/document/page|:heavy_check_mark:|:x:|:x:|
|Automates|:heavy_check_mark:|:x:|:x:|
|Tags - assign colored tags to documents or folders|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|Documents and Folders|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|Multi-User|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|User permissions management|:heavy_check_mark:|:heavy_check_mark:|:x:|
|Document permissions management|:heavy_check_mark:|:x:|:x:|
|REST API|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|Page Delete/Reorder/Move|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|Page Rotation|:x:|:heavy_check_mark:|:heavy_check_mark:|
|Documents Merging|:x:|:heavy_check_mark:|:heavy_check_mark:|
|Cloud Native/K8s Support|:x:|:heavy_check_mark:|:heavy_check_mark:|
