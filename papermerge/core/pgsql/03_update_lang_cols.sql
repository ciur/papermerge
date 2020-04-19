UPDATE core_page 
SET text_fts=setweight(
    to_tsvector(core_languagemap.pg_catalog, coalesce(text,'')),
    'C'
)
FROM core_languagemap
WHERE core_languagemap.tsr_code = core_page.lang;


UPDATE core_basetreenode 
SET title_fts=setweight( 
    to_tsvector(
        core_languagemap.pg_catalog,
        coalesce(
            regexp_replace(title, '[^[:alnum:]]', ' ', 'g'),
            ''
        )
    ),
    'A'
)
FROM core_languagemap
WHERE core_languagemap.tsr_code = core_page.lang;


UPDATE core_basetreenode as node
SET ancestors_fts = ancestors_to_tsvector(
        core_languagemap.pg_short,
        get_ancestors(node.id)
    )
FROM core_languagemap
WHERE core_languagemap.tsr_code = core_page.lang;