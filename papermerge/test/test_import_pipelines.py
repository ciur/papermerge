from django.test import TestCase


PAPERMERGE_PIPELINES = [
    'papermerge.test.test_import_pipelines.PipelineOne',
    'papermerge.test.test_import_pipelines.PipelineTwo',
    'papermerge.test.test_import_pipelines.PipelineThree',
]


class TestImportPipelines(TestCase):
    pass


class PipelineOne:

    def get_init_kwargs(self):
        if self.doc:
            return {'doc': self.doc}
        return None

    def get_apply_kwargs(self):
        if self.doc:
            return {'doc': self.doc}
        return None

    def apply(self):
        pass


class PipelineTwo:
    pass


class PipelineThree:
    pass
