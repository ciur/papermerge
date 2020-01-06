

"""
    WITH summary AS (
        SELECT
            node_id,
            title,
            ctype,
            page_num,
            page_rank,
            page_highlight,
            ROW_NUMBER() OVER(
                PARTITION BY
                subq.node_id ORDER BY subq.page_rank DESC,
                subq.page_num
            ) AS rk
        FROM (
            SELECT
                node.id AS node_id,
                node.title AS title,
                node.polymorphic_ctype_id AS ctype,
                page.number AS page_num,
                ts_rank_cd(
                    (
                        // var language
                        COALESCE(node.title_deu, '') ||
                        COALESCE(node.ancestors_deu, '') ||
                        COALESCE(page.text_deu, '')
                    ),
                    websearch_to_tsquery(
                        'german'::regconfig, // var language
                        'Oracle or exit'
                    ),
                    32
                ) AS page_rank,
                ts_headline(
                    'german',
                    page.text,
                    plainto_tsquery(
                        'german'::regconfig, // var language
                        'Oracle or exit'
                    ),
                   'MaxWords = 30, MinWords = 15, MaxFragments = 1'
                ) AS page_highlight
            FROM core_basetreenode node
            LEFT OUTER JOIN core_document doc ON (
                doc.basetreenode_ptr_id = node.id
            )
            LEFT OUTER JOIN core_page page ON (
                page.document_id = doc.basetreenode_ptr_id
            )
            WHERE node.id IN (1, 2, 3) // may or may not be present
        ) subq
    )
    SELECT
        s.node_id as id,
        s.page_highlight as page_highlight
    FROM summary s
    WHERE s.rk = 1 and page_rank > 0.1
    ORDER BY s.ctype desc, s.page_rank DESC
"""


def get_search_sql(lang, desc_filter=[]):
    title = {
        'deu': 'title_deu',
        'eng': 'title_eng'
    }
    ancestors = {
        'deu': 'ancestors_deu',
        'eng': 'ancestors_eng'
    }
    text = {
        'deu': 'text_deu',
        'eng': 'text_eng',
    }
    language = {
        'deu': 'german',
        'eng': 'english'
    }
    ts_rank_cd = f"""
        (
            COALESCE(node.{title[lang]}, '') ||
            COALESCE(node.{ancestors[lang]}, '') ||
            COALESCE(page.{text[lang]}, '')
        ),
        websearch_to_tsquery(
            '{language[lang]}'::regconfig,
            %(search_term)s
        ),
        32
    """
    ts_headline = f"""
        '{language[lang]}',
        page.text,
        plainto_tsquery(
            '{language[lang]}'::regconfig,
            %(search_term)s
        ),
       'MaxWords = 20, MinWords = 15, MaxFragments = 2'
    """
    optional_where = ""

    if len(desc_filter) > 0:
        optional_where = f"""
            WHERE node.id IN ({','.join(desc_filter)})
        """
    sql = f"""
    WITH summary AS (
        SELECT
            node_id,
            title,
            model_ctype,
            page_num,
            page_rank,
            page_highlight,
            ROW_NUMBER() OVER(
                PARTITION BY
                subq.node_id ORDER BY subq.page_rank DESC,
                subq.page_num
            ) AS rk
        FROM (
            SELECT
                node.id AS node_id,
                node.title AS title,
                ctype.model AS model_ctype,
                page.number AS page_num,
                ts_rank_cd (
                    {ts_rank_cd}
                ) AS page_rank,
                ts_headline(
                    {ts_headline}
                ) AS page_highlight
            FROM core_basetreenode node
            LEFT OUTER JOIN core_document doc ON (
                doc.basetreenode_ptr_id = node.id
            )
            LEFT OUTER JOIN core_page page ON (
                page.document_id = doc.basetreenode_ptr_id
            )
            LEFT OUTER JOIN django_content_type ctype ON (
                node.polymorphic_ctype_id = ctype.id
            )
            {optional_where}
        ) subq
    )
    SELECT
        s.node_id as id,
        s.page_highlight as page_highlight,
        s.model_ctype as model_ctype
    FROM summary s
    WHERE s.rk = 1 and page_rank > 0.001
    ORDER BY s.model_ctype desc, s.page_rank DESC
    """
    return sql

