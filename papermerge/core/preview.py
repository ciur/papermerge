from django.urls import reverse


class PreviewUrlsHandover:
    """
    Generate all preview urls for given document id.

    Generated urls might be passed to static js code in order
    to enpower javasscript code the initiation of previews.
    """

    def __init__(
        self,
        document_id,
        page_count
    ):
        self.document_id = document_id
        self.page_count = page_count

    def __iter__(self):
        for index in range(1, self.page_count + 1):
            doc_id = self.document_id
            for step in range(0, 4):
                yield(
                    (
                        index,
                        step,
                        reverse('core:preview', args=[doc_id, step, index]))
                )
