#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.test

./manage.py test $@ # papermerge.test.test_access_model \
                 # papermerge.test.test_access_view \
                 # papermerge.test.test_hocr \
                 # papermerge.test.test_search \
                 # papermerge.test.test_search_excerpt \
                 # papermerge.test.test_path \
                 # papermerge.test.test_page \
                 # papermerge.test.test_document \
                 # papermerge.test.test_document_view \
                 # papermerge.test.test_folder \
                 # papermerge.test.test_typed_key \
                 # papermerge.test.test_search_excerpt \
                 # papermerge.test.test_node \
                 # papermerge.test.test_kvstore
