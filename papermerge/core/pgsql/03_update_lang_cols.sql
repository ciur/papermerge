UPDATE core_page 
SET text_deu=setweight(
    to_tsvector('pg_catalog.german', coalesce(text,'')),
    'C'
)
WHERE lang = 'deu';

UPDATE core_page 
SET text_eng=setweight(
    to_tsvector('pg_catalog.english', coalesce(text,'')),
    'C'
)
WHERE lang = 'eng';

UPDATE core_basetreenode 
SET title_deu=setweight(
    to_tsvector(
        'pg_catalog.german',
        coalesce(
            regexp_replace(title, '[^[:alnum:]]', ' ', 'g'),
            ''
        )
    ),
    'A'
)
WHERE lang = 'eng';

UPDATE core_basetreenode 
SET title_eng=setweight(
    to_tsvector(
        'pg_catalog.english',
        coalesce(
            regexp_replace(title, '[^[:alnum:]]', ' ', 'g'),
            ''
        )
    ),
    'A'
)
WHERE lang = 'eng';

UPDATE core_basetreenode as node
SET ancestors_deu = ancestors_to_tsvector(
        'german',
        get_ancestors(node.id)
    )
WHERE lang = 'deu';

UPDATE core_basetreenode as node
SET ancestors_eng = ancestors_to_tsvector(
        'english',
        get_ancestors(node.id)
    )
WHERE lang = 'eng';