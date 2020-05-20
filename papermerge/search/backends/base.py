from papermerge.search.index import class_is_indexed, get_indexed_models


class NullIndex:
    """
    Index class that provides do-nothing implementations of the indexing
    operations required by BaseSearchBackend. Use this for search backends
    that do not maintain an index, such as the database backend.
    """

    def add_model(self, model):
        pass

    def refresh(self):
        pass

    def add_item(self, item):
        pass

    def add_items(self, model, items):
        pass

    def delete_item(self, item):
        pass


class BaseSearchBackend:
    query_compiler_class = None
    autocomplete_query_compiler_class = None
    results_class = None
    rebuilder_class = None

    def __init__(self, params):
        pass

    def get_index_for_model(self, model):
        return NullIndex()

    def get_rebuilder(self):
        return None

    def reset_index(self):
        raise NotImplementedError

    def add_type(self, model):
        self.get_index_for_model(model).add_model(model)

    def refresh_index(self):
        refreshed_indexes = []
        for model in get_indexed_models():
            index = self.get_index_for_model(model)
            if index not in refreshed_indexes:
                index.refresh()
                refreshed_indexes.append(index)

    def add(self, obj):
        self.get_index_for_model(type(obj)).add_item(obj)

    def add_bulk(self, model, obj_list):
        self.get_index_for_model(model).add_items(model, obj_list)

    def delete(self, obj):
        self.get_index_for_model(type(obj)).delete_item(obj)

    def _search(self, query_compiler_class, query, model_or_queryset, **kwargs):
        # Find model/queryset
        if isinstance(model_or_queryset, QuerySet):
            model = model_or_queryset.model
            queryset = model_or_queryset
        else:
            model = model_or_queryset
            queryset = model_or_queryset.objects.all()

        # Model must be a class that is in the index
        if not class_is_indexed(model):
            return EmptySearchResults()

        # Check that theres still a query string after the clean up
        if query == "":
            return EmptySearchResults()

        # Search
        search_query = query_compiler_class(
            queryset, query, **kwargs
        )

        # Check the query
        search_query.check()

        return self.results_class(self, search_query)

    def search(self, query, model_or_queryset, fields=None, operator=None, order_by_relevance=True, partial_match=True):
        return self._search(
            self.query_compiler_class,
            query,
            model_or_queryset,
            fields=fields,
            operator=operator,
            order_by_relevance=order_by_relevance,
            partial_match=partial_match,
        )