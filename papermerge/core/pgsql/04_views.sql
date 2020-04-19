/**
Following query:

SELECT * 
FROM document_pages
WHERE id = doc_id

id is same as core_basetreenode.id or doc.basetreenode_ptr_id,
will provide quickly most important info about doc_id.
**/

DROP VIEW IF EXISTS document_pages;
CREATE OR REPLACE VIEW document_pages AS
SELECT 
    node.id AS id,
    node.title AS title,
    node.user_id AS user_id,
    doc.text_fts AS text_fts,
    doc.notes AS notes,
    doc.file_name AS file_name,
    page.id AS page_id, 
    page.number AS page_number,
    doc.page_count AS page_count_from_doc,
    page.page_count AS page_count,
    page.text_fts AS page_text_fts
FROM core_basetreenode node
LEFT OUTER JOIN core_document doc ON (doc.basetreenode_ptr_id = node.id)
LEFT OUTER JOIN core_page page ON (doc.basetreenode_ptr_id = page.document_id)
LEFT OUTER JOIN django_content_type ctype ON (ctype.id = node.polymorphic_ctype_id)
WHERE ctype.model = 'document';


DROP VIEW IF EXISTS node_access;
CREATE OR REPLACE VIEW node_access AS
SELECT
    u.username,
    n.id as node_id,
    n.title as node_title,
    acc.id as access_id,
    acc.access_type,
    acc.access_inherited,
    perm.codename,
    perm.id as perm_id
FROM core_basetreenode n
LEFT JOIN core_access acc ON n.id = acc.node_id
LEFT JOIN core_user u ON u.id = n.user_id
LEFT JOIN core_access_permissions acc_perm ON acc_perm.access_id = acc.id
LEFT JOIN auth_permission perm ON perm.id = acc_perm.permission_id
ORDER BY u.username, n.title;

DROP VIEW IF EXISTS table_size;
CREATE OR REPLACE VIEW table_size AS
SELECT 
schemaname AS table_schema,
relname AS table_name,
pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
pg_size_pretty(pg_relation_size(relid)) AS data_size,
pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS external_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC, pg_relation_size(relid) DESC;