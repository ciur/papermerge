import logging

logger = logging.getLogger(__name__)


def get_fields(model):
    """
    Returns django fields of current ``model``.

    Does not include inherited fields.
    """
    return model._meta.get_fields(include_parents=False)


def group_per_model(models, **kwargs):
    """
    groups kwargs per model

    What this method is supposed to do is better exmplained by example.
    Suppose there are 3 models i.e. ``models`` list contains
    3 models: [Model_1, Model_2, Model_3]. Each of these models
    has following django field attributes:

        class Model_1:
            attr_m1_a
            attr_m1_b

        class Model_2:
            attr_m2_x

        class Model_3:
            attr_m3_j
            attr_m3_k

    kwargs_ex_1 = {
        'blah': 1, 'extra': 2, 'attr_m1_a': "see?", 'attr_m1_b': "this?"
    }

    group_per_model(models, **kwargs_ex_1) will return:

        {
            Model_1: {'attr_m1_a': "see?", 'attr_m1_b': "this?"}
        }

    kwargs_ex_2 = {
        'blah': 1, attr_m1_a': "AB", 'attr_m2_x': "XX"
    }
    group_per_model(models, **kwargs_ex_2) will return:

        {
            Model_1: {'attr_m1_a': "AB"}
            Model_2: {'attr_m2_x': "XX"}
        }
    """
    ret = {}

    for model in models:
        fields = get_fields(model)
        for field in fields:
            if field.name in kwargs.keys():
                ret.setdefault(model, {}).update(
                    {field.name: kwargs[field.name]}
                )

    return ret
