from django.dispatch import Signal

page_hocr_ready = Signal(
    providing_args=[
        "user_id",
        "document_id",
        "page_num",
        "lang"
    ]
)

# Sent by core.views.documents.create_folder
# Sent AFTER one single folder was created
folder_created = Signal(
    providing_args=[
        "user_id",
        "level",
        "message",
        "folder_id"
    ]
)

# Sent by core.views.nodes.nodes_view
# Sent AFTER one of more nodes were batch deleted
nodes_deleted = Signal(
    providing_args=[
        "user_id",
        "level",
        "message",
        # node tags is a list of
        # '<a href="{node.id}">{node.title}</a>'
        "node_tags"
    ]
)

