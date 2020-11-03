import inspect

from django.apps import apps


class PartsFinder:
    """
    Finds models descending from one of:

        (1) papermerge.core.models.AbstractNode
        (2) papermerge.core.models.AbstractDocument
        (3) papermerge.core.models.AbstractFolder

    Looks for model candidates in all (current django) project apps.
    Models descending from (1), (2) ,(3) are called parts.
    """

    def find(self, abstract_klass):
        """
        Returns all models descendent from given ``abstract_klass``
        """
        app_configs = apps.get_app_configs()
        ret = []

        for app_config in app_configs:
            app_models = app_config.get_models()

            for model_klass in app_models:
                if self.descents_from_abstract(model_klass, abstract_klass):
                    ret.append(model_klass)

        return ret

    def get(self, abstract_klass, attr_name):
        """
        Returns model_klass which inherits from ``abstract_klass``
        AND has attribute ``attr_name``
        """
        all_parts = self.find(abstract_klass)

        for model_klass in all_parts:
            if hasattr(model_klass, attr_name):
                return model_klass

    def descents_from_abstract(self, klass, abstract_klass):
        """
        Is ``klass`` descending from ``abstract_klass``?
        """
        return abstract_klass in inspect.getmro(klass)


def get_parts_finder_class():
    return PartsFinder


parts_finder_class = get_parts_finder_class()

default_parts_finder = parts_finder_class()
