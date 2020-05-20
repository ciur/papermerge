from django.db.models.query import QuerySet
from papermerge.search.index import class_is_indexed, get_indexed_models


class BaseSearchResults:
    supports_facet = False

    def __init__(self, backend, query_compiler, prefetch_related=None):
        self.backend = backend
        self.query_compiler = query_compiler
        self.prefetch_related = prefetch_related
        self.start = 0
        self.stop = None
        self._results_cache = None
        self._count_cache = None
        self._score_field = None

    def _set_limits(self, start=None, stop=None):
        if stop is not None:
            if self.stop is not None:
                self.stop = min(self.stop, self.start + stop)
            else:
                self.stop = self.start + stop

        if start is not None:
            if self.stop is not None:
                self.start = min(self.stop, self.start + start)
            else:
                self.start = self.start + start

    def _clone(self):
        klass = self.__class__
        new = klass(self.backend, self.query_compiler,
                    prefetch_related=self.prefetch_related)
        new.start = self.start
        new.stop = self.stop
        new._score_field = self._score_field
        return new

    def _do_search(self):
        raise NotImplementedError

    def _do_count(self):
        raise NotImplementedError

    def results(self):
        if self._results_cache is None:
            self._results_cache = list(self._do_search())
        return self._results_cache

    def count(self):
        if self._count_cache is None:
            if self._results_cache is not None:
                self._count_cache = len(self._results_cache)
            else:
                self._count_cache = self._do_count()
        return self._count_cache

    def __getitem__(self, key):
        new = self._clone()

        if isinstance(key, slice):
            # Set limits
            start = int(key.start) if key.start else None
            stop = int(key.stop) if key.stop else None
            new._set_limits(start, stop)

            # Copy results cache
            if self._results_cache is not None:
                new._results_cache = self._results_cache[key]

            return new
        else:
            if self._results_cache is not None:
                return self._results_cache[key]

            new.start = self.start + key
            new.stop = self.start + key + 1
            return list(new)[0]

    def __iter__(self):
        return iter(self.results())

    def __len__(self):
        return len(self.results())

    def __repr__(self):
        data = list(self[:21])
        if len(data) > 20:
            data[-1] = "...(remaining elements truncated)..."
        return '<SearchResults %r>' % data

    def annotate_score(self, field_name):
        clone = self._clone()
        clone._score_field = field_name
        return clone

    def facet(self, field_name):
        raise NotImplementedError(
            "This search backend does not support faceting"
        )


class EmptySearchResults(BaseSearchResults):
    def __init__(self):
        super().__init__(None, None)

    def _clone(self):
        return self.__class__()

    def _do_search(self):
        return []

    def _do_count(self):
        return 0


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

    def _search(
        self,
        query_compiler_class,
        query,
        model_or_queryset,
        **kwargs
    ):
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

    def search(
        self,
        query,
        model_or_queryset,
        fields=None,
        operator=None,
        order_by_relevance=True,
        partial_match=True
    ):
        return self._search(
            self.query_compiler_class,
            query,
            model_or_queryset,
            fields=fields,
            operator=operator,
            order_by_relevance=order_by_relevance,
            partial_match=partial_match,
        )
