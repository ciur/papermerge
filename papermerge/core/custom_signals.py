from django.dispatch import Signal

# signal sent when either Folder or Document adds/deletes/updates its KVS
# so that all interested parties (descendent nodes and pages) will
# update accordingly
propagate_kv = Signal()
