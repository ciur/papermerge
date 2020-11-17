
def sanitize_kvstore_list(kvstore_list):
    """
    Creates a new dictionay only with allowed keys.
    """
    new_kvstore_list = []
    allowed_keys = [
        'id',
        'key',
        'value',
        'kv_type',
        'kv_format',
        'kv_inherited',
    ]

    for item in kvstore_list:
        sanitized_kvstore_item = {
            allowed_key: item.get(allowed_key, None)
            for allowed_key in allowed_keys
            if allowed_key in item.keys()
        }
        new_kvstore_list.append(sanitized_kvstore_item)

    return new_kvstore_list
