import logging


logger = logging.getLogger(__name__)


class ClipboardPages:

    def __init__(self, session, user_id):
        self._dict = {}
        self._session = session
        self._user_id = user_id

    @property
    def clipboard_id(self):
        return f"{self._user_id}.clipboard.nodes"

    def update_session(self):
        pass

    def clear(self):
        self._dict = {}
        self.clear_session()
        logger.debug("ClipboardPages cleared.")

    def add(self, doc_id, page_nums):
        if not self._dict.get(doc_id, False):
            self._dict[doc_id] = set()

        self._dict[doc_id].update(page_nums)

        self.update_session()

    def all(self):
        pass


class ClipboardNodes:

    def __init__(self, session, user_id):
        self._set = set()
        self._session = session
        self._user_id = user_id

    def clear(self):

        self._set.clear()
        self.clear_session()
        logger.debug("ClipboardNodes cleared.")

    @property
    def clipboard_id(self):
        return f"{self._user_id}.clipboard.nodes"

    def update_session(self):
        self._session[self.clipboard_id] = list(self._set)

    def clear_session(self):
        self._session[self.clipboard_id] = []

    def add(self, items):

        logger.debug(f"Add items={items} to {self}")

        self._set.update(items)

        logger.debug(self)

        self.update_session()

    def all(self):
        return self._session[self.clipboard_id]

    def __str__(self):
        return f"ClipboardNodes({self.clipboard_id}, {self._set})"


class Clipboard:

    def __init__(self, session, user_id):
        self.pages = ClipboardPages(session, user_id)
        self.nodes = ClipboardNodes(session, user_id)
        self.session = session
        self.user_id = user_id

    def clear(self):
        self.pages.clear()
        self.nodes.clear()


class ClipboardMiddleware:
    """
    Manages clipboard of document and pages.
    Clipboard operates only with IDs (or page order numbers).

    Adds a clipboard attribute to request object.

    * Resets/Delets everything (for current user) from clipboard:

        request.clipboard.reset()

    * Get cliboard object for currently logged in user:

        request.clipboard.all()

    returns:

        {
            'nodes': ['node1', 'node2', 'node3'], # <- whole nodes to be pasted
            'pages': { # <- pages to be pasted (with their docs)
                'doc_id1': [page1, page2]
                'doc_id2': [page1]
            }
        }

    page1, page2, ... ARE PAGE ORDERs (page1 = 1 => first page)

    * Get current nodes in clipboard:

        request.clipboard.nodes.all()

    returns and array/list of node ids currently in clipboard

        ['node1', 'node2', ...]

    * Adds node ids into the clipboard. Node is a folder or a document's id:

        request.clipboard.nodes.add(1, 2, 3, 4)
        request.clipboard.nodes.add([1, 2, 3, 4])

    * Get pages currently in clipboard (for current user):

        request.cliboard.pages.all()

    returns:
        {
            'doc_id1': [page1, page2, page3],
            'doc_id2': [page1, page2, page3]
        }

        again, page1, page2 etc are page order numbers


    * Adds pages and their documents into the clipboard:

        request.clipboard.pages.add(1, [1, 2, 3])
        request.clipboard.pages.add(1, 1, 2, 3)

    first agrument is the document id. Rest of the arguments are
    page order numbers.

    Can be written as:

        request.clipboard.pages.add(doc=1, pages=[1, 2, 3])
        request.clipboard.pages.add(doc=1, page=2)

    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        if request.user:
            # clipboard is per user. It makes sense only
            # when there is a logged in
            request.clipboard = Clipboard(
                session=request.session,
                user_id=request.user.id
            )
            # shortcuts
            request.nodes = request.clipboard.nodes
            request.pages = request.clipboard.pages
        response = self.get_response(request)

        return response
