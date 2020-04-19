UPDATE core_page 
SET text_fts=setweight(
    to_tsvector(core_languagemap.pg_catalog::regconfig, coalesce(text,'')),
    'C'
)
FROM core_languagemap
WHERE core_languagemap.tsr_code = core_page.lang;


UPDATE core_basetreenode 
SET title_fts=setweight( 
    to_tsvector(
        core_languagemap.pg_catalog::regconfig,
        coalesce(
            regexp_replace(title, '[^[:alnum:]]', ' ', 'g'),
            ''
        )
    ),
    'A'
)
FROM core_languagemap
WHERE core_languagemap.tsr_code = core_basetreenode.lang;


UPDATE core_basetreenode as node
SET ancestors_fts = ancestors_to_tsvector(
        core_languagemap.pg_short::regconfig,
        get_ancestors(node.id)
    )
FROM core_languagemap
WHERE core_languagemap.tsr_code = node.lang;