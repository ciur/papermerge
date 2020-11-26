# We :heart: Your Contributions

Thank you for taking your time to contribute to Papermerge. This guide will
help you spend your time well, and help us keep Papermerge focused and making
valuable progress.

In general, for very small changes like fixing documentation typo, remove
unused variable or just remove a redundant white space - just create a pull
request and very likely that your change (if it is reasonable) will be
accepted immediately.

For more **significant changes**, for example you plan to add a feature, or
change/add a whole paragraph to the documentation - please **first discuss the
change** you wish to make via GitHub issue, pull request or
[email](mailto:eugen@papermerge.com).

As general rule: the smaller your pull request is - the higher chance of it
being merged.


## Fix a Typo

Contribute to the project just by fixing documentation's typos. Like tis one. English is not [project maintainer's](https://github.com/ciur/) native lnguage so he makes lots of typoz.

Fixing documentation typos is easiest and fastest way to value to the project. 

## Open an Issue.

Another way to contribute is open issues. Obviously this means you need to at
least run once application and test it.


## Translate

Currently Papermerge's user interface is available in English and German.

If your master another language (e.g French, Spanish, Russian etc)
you can add great value to the project by translating it to your own native
language. Because Papermerge is based on absolutely awesome [Django Web
Framework](https://www.djangoproject.com/) all Django's documentation applies
here as well. So it is a good idea to first go through [Django's i18n
documentation](https://docs.djangoproject.com/en/3.1/topics/i18n/) and then
come back to translation Papermerge specific topics.

For detailed information check [Translators Guide in
documentation](https://papermerge.readthedocs.io/en/latest/translators_guide/index.html).


## Fixes and Pull Requests

If you want to contribute (fix a bug, add a feature) - that is absolutely great!
Any kind of improvement is welcome.

There are 3 golden rules to follow.


### Rule 1 (R1)

PEP8.

All code must formated with [PEP8
style](https://www.python.org/dev/peps/pep-0008/). If you code has couple of
minor deviations from PEP8 - that's ok. We are flexible here, but if your PR code formatting 
has serious violations of PEP8 - it will simply be rejected with comment *not PEP8 formatted*.


### Rule 2 (R2)

Communicate. Document.

**Before creating a pull request for a new feature** - please first discuss the
change you wish to make via GitHub issue, pull request or email. A
silent creation of PR for any sort of feature without any communication will
result in silent discard of your PR. If you are lazy to comment you your PR -
why should we care to communicate you the reason of rejection? :))


### Rule 3 (R3)

Test. Test. Test.

Code without tests is broken design.
New features without basic tests will be rejected.


## For Developers. Regarding Code Style - Far Beyond PEP8

Papermerge code has a style. You may not like it, because style is a matter of
taste after all. However, for the sake of consistency - you will need to
follow couple of extra rule. Following rules are not so strict as 3 golden
rules above (1. PEP8, 2. Document 3. Test) however you are strongly encouraged
to follow them.

### Use fStrings (S1)

Use fStrings whenever possible.

Bad:

    logger.debug("{} importer: not a file.".format(processor))

Good:

    logger.debug(
        f"{processor} importer: not a file."
    )