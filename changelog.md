# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

Initial commit. Project started as free time pet project.
It was named vermilion, digilette and only later papermerge.

