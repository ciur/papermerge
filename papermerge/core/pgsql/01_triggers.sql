CREATE OR REPLACE FUNCTION core_page_trigger() RETURNS trigger AS $$
DECLARE
    pg_catalog_name varchar(64);
BEGIN
    SELECT core_languagemap.pg_catalog
    INTO pg_catalog_name
    FROM core_languagemap
    WHERE core_languagemap.tsr_code = new.lang;

    new.text_fts := 
     setweight(
        to_tsvector(
            pg_catalog_name, coalesce(new.text,'')
        ),
        'C'
    );

    RETURN new;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION core_basetreenode_trigger() RETURNS trigger AS $$
DECLARE
    pg_catalog_name varchar(64);
BEGIN
    
    SELECT core_languagemap.pg_catalog
    INTO pg_catalog_name
    FROM core_languagemap
    WHERE core_languagemap.tsr_code = new.lang;

    new.title_tsr :=
     setweight(
        to_tsvector(
            pg_catalog_name, 
            coalesce(
                regexp_replace(new.title, '[^[:alnum:]]', ' ', 'g'),
            '')
        ),
    'A');

    RETURN new;
END
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS tsvector_update_core_page ON core_page;
CREATE TRIGGER tsvector_update_core_page BEFORE INSERT OR UPDATE
    ON core_page FOR EACH ROW EXECUTE PROCEDURE core_page_trigger();

DROP TRIGGER IF EXISTS tsvector_update_core_basetreenode ON core_basetreenode;
CREATE TRIGGER tsvector_update_core_basetreenode BEFORE INSERT OR UPDATE
    ON core_basetreenode FOR EACH ROW EXECUTE PROCEDURE core_basetreenode_trigger();


