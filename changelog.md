# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2024-01-13

### Fixed

- Django ORM leaves DB connections open [Issue#575](https://github.com/ciur/papermerge/issues/575)
- Add extra language codes [Issue#571](https://github.com/ciur/papermerge/issues/571)
- Create user/home/folder in one DB transaction [Issue#572](https://github.com/ciur/papermerge/issues/572)

## [2.0.1] - 9 April 2021

### Changed

- Django dependency version bumped from 3.1.7 to 3.2 


## [2.0.0] - 31 March 2021

### Changed

- Issue #354 fixed - scroll not working on search result page
- Issue #349 fixed - pagination for pinned tags does not work
- Issue #350 fixed - Umlauts don't work
- Issue #339 fixed - IMAP import from gmail isn't working
- Issue #338 fixed - Reflected Cross-Site Scripting (XSS) in Upload Error Messages 


## [2.0.0rc48] - 12 March 2021

### Changed

- Issue #281 fixed - IMPORT_MAIL_DELETE not working 
- Issue #233 fixed - IMAP Consumption - Mails imported multiple times and not marked as read 
- Automated docker images build & push


## [2.0.0rc45] - 5 March 2021

- Fixes version issue (documents created by paste opreration should have version reset to 0)


## [2.0.0.rc38] - 28 February 2021

### Changed

- Issue #311 - Fixes upgrade problems (migrations conflicts)
- Issue #314 - Cross-Site Scripting (XSS) in Automation Tags
- Issue #315 - Bug leads to multiple folder creation 
- Issue #316 - Cross-Site Scripting (XSS) in Permission Management


## [2.0.0.rc35] - 25 February 2021

### Added

- Apps support (document parts/satellites architecture)
- UI preferences - user can set timezone, date, time format from UI: user -> preferences 
- UI design improvements - widgets sidebar
- UX improvement - action button was replaced with (desktop like) context menu 
- UX improvement - Desktop like selection
- Import Pipeline - flexible import framework - thanks to [Francesco](https://github.com/francescocarzaniga)
- Email inbox enhancement (IMPORT_MAIL_BY_USER) - thanks to [Francesco](https://github.com/francescocarzaniga)
- no more pdftk dependency. For pdf operations will use [stapler](https://github.com/hellerbarde/stapler/) instead.
- Roles - quicker way to assign set of permissions for a given user
- Document versions (all changes on the document are non-distructively saved)
- User can manually re-run automates
- User can manually re-start OCR for selected documents
- In document viewer user can see OCRed page text


[1.5.5] - 27 December 2020

### Added

- Fixes #271 - XSS on tag's description field.
- No more failing test in ./run_tests.sh see #272 for details
- Fixes #198 - docker compose configuration uses redis for message brocker


### [1.5.4] - 23 December 2020

### Added

- Fix for #261 - docker-compose sample doesn't set-up fully
- Fix for #241 - App Docker Tag 1.5.3 seems to be the worker?
- Fix for #237 - Cannot rename folder
- Fix for #239 - Adjusting size of sign-in button
- Fix for #243 - Automates Screen max items
- Fix for #257 - Using browser back/foward navigation causes json strings to be displayed instead of documents.


## [1.5.3] - 1 December 2020

### Added

- Fix for #237 - Renaming files problem.

## [1.5.2] - 30 November 2020

This is security release.

### Added

- Extra fixes for #228 - Stored Cross-Site Scripting (XSS). Thanks to [@l4rm4nd](https://github.com/l4rm4nd) for security audit.

## [1.5.1] - 29 November 2020
    
### Added
    
- Fixes #204 - Groups are not created
- Fixes #206 - Anonymous user access to breadcrumb results in 500
- Fixes #208 - Tags unique per user (different users can have tags with same name)
- Fixes #202 - Automates created for all users
- Fixes #185 - inbox folder is only selectable at automate creation
- Fixes #196 - Allow Automates to only apply tags or move to folder
- Fixes #228 - Stored Cross-Site Scripting (XSS)


## [1.5.0] - 14 October 2020

## [1.5.0.rc1] - 11 October 2020

### Added

- Additional languages included in default configuration of official docker image.
- MySQL Support. Fixes #76.
- Fixes #150 (Directory Navigation)
- Download multiple documents and folders. Fixes #84.
- Auto-refresh on upload fixes #126
- add "--include-user-password" switch to backup scripts
- include tags into backups    
- Tag management (colored tags)
- Pinnable tags
- Better selection. Selection All/Folders/Documents/Invert Selection/Deselect menu.
- Extra check (./manage.py check) for IMAP credentials. In case IMAP settings are not correct, ./manage.py check will issue a warning message. Also imap import will complain if IMAP credentials are incorrect. Extra detailed debugging messages for IMAP import.
- Tags per Automate (matching docs will be assigned automate's tags)

### Changed

- Upgrade to django 3.0.10
- Dynamic preferences upgraded to latest 1.10.1 version
- Fixes issue #120 REST API fails when uploading a document
- Issue #114 Worker container use environment variables for DB
- For backup/restore scripts --user argument is optional. Without --user argument backup command will backup all users' documents.
- Fixes issue #118 - Email Import does not reach INBOX.

### Removed

- Metadata plugins as Python modules. In future will be replaced with yml templates.


## [1.4.4] - 28 September 2020

### Changed

- Fixes issue #118 - Email Import does not reach INBOX.
- 3rd party apps/plugins can extend user menu


## [1.4.3] - 16 September 2020

### Changed

- Fixes issue #120 REST API fails when uploading a document
- Issue #114 Worker container use environment variables for DB
- For backup/restore scripts --user argument is optional. Without --user argument backup command will backup all users' documents.
- Extra check (./manage.py check) for IMAP credentials. In case IMAP settings are not correct, ./manage.py check will issue a warning message. Also imap import will complain if IMAP credentials are incorrect. Extra detailed debugging messages for IMAP import.

## [1.4.2] - 6 September 2020

### Added

- UI logs. A mini-feature. It helps user to troubleshoot/get feedback from not
    directly visible processes like running automates or background OCRing of
    the docs
- Automates match by txt not by hocr file
- Clipboard bugfixes
- Display current version at the lower/right bottom
- Bug fixes


## [1.4.1] - 29 August 2020

### Removed

- startetc command was removed.

### Added

- Optimizations/performance issues - browsing folder with many files (> 200)
 was improved significantly (5x). Also, /browse/ request time will not linearly grow with increased number of files.

### Changed

- Do not rise exception if preview image was not found. Return a generic image instead.
- Fix: [issue #86](https://github.com/ciur/papermerge/issues/86) - UI uploader - confusing red color/warning during upload
- Enhancement: in case of uploading unsupported format - a descriptive error message will be displayed in uploader
- Documentation updates (especially [bare metal installation](https://papermerge.readthedocs.io/en/latest/setup/manual_way.html) + [server configuration](https://papermerge.readthedocs.io/en/latest/setup/server_configurations.html))


## [1.4.0] - 19 August 2020

### Changed
    
- Issue #72 - random changed order
- Issue #63 - hardcoded OCR_BINARY settings
- documentation updates

## [1.4.0.rc1] - 4 August 2020

### Added 

- Automation (of metadata extraction, moving doc to a specific folder, extract page)
- AdminLTE3/Bootstrap based own UI
- Backup/Restore feature. Feature implemented by [@frenos](https://github.com/frenos).
- Added support for JPEG, PNG, TIFF images

### Changed

- Metadata details are now displayed/edited on specialized right side panel (instead of modals)

### Removed

- Customized Django Admin app named boss. Thus, UI is no longer Django Admin based.



## [1.3.0] - 25 June 2020

### Added

- Metadata (per Folder/Document/Page)
- Built-in worker (./manage.py worker - command)

### Changed


- SQLite is default database (Postresql is now optional, available via Plugin)
- Support for OCR on all languages
- Refactoring: all static assets moved into boss/static directory. This change simplifies initial project setup (no need to clone yet another repo)
- Read configurations from /etc/papermerge.conf.py or ./papermerge.conf.py
- Refactoring: endpoint extracted from pmworker into mglib.path.DocumentPath and mglib.path.PagePath
- Save last sorting mode in file browser - via save_last_sort cookie


## [1.2.0] - 10 Apr 2020

### Added

- Delete pages
- Reorder pages within the document 
- Cut/Paste document from one document into another
- Paste pages into new document instance

### Changed

- [Documentation](https://papermerge.readthedocs.io/en/v1.2.0/page_management.html) - updated to include Page Management feature description

## [1.1.0] - 14 Feb 2020

### Added

- REST API support
- Creation of multiple authentication tokens per user
- Endpoint /api/document/upload for uploading documents
- Rest API [feature demo ](https://www.youtube.com/watch?v=OePTvPcnoMw)

### Changed

- [Documentation](https://papermerge.readthedocs.io/en/v1.1.0/rest_api.html) - updated to include REST API description

## [1.0.0] - 7 Feb 2020

Open sourced version is more or less stable.

## [0.5.0] - 6 Jan 2020

Project open sourced (also with lots of refactoring)

## [0.0.1] - 10 Sept 2017

Initial commit. Project started as free time pet project / proof of concept.
It was named vermilion, digilette and only later papermerge.
