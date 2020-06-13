from django.dispatch import Signal

page_hocr_ready = Signal(
    providing_args=[
        "user_id",
        "document_id",
        "page_num",
        "lang"
    ]
)
