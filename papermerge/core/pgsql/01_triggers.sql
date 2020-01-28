CREATE OR REPLACE FUNCTION core_page_trigger() RETURNS trigger AS $$
begin
    IF new.lang = 'deu'
    THEN
        new.text_deu :=
         setweight(
            to_tsvector(
                'pg_catalog.german', coalesce(new.text,'')
            ),
            'C'
        );
      
    ELSE
        new.text_eng :=
            setweight(
                to_tsvector(
                    'pg_catalog.english', coalesce(new.text,'')
                ),
                'C'
            );
    END IF;

    RETURN new;
end
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION core_basetreenode_trigger() RETURNS trigger AS $$
begin
    IF new.lang = 'deu'
    THEN
        new.title_deu :=
         setweight(
            to_tsvector(
                'pg_catalog.german', 
                coalesce(
                    regexp_replace(new.title, '[^[:alnum:]]', ' ', 'g'),
                '')
            ),
        'A');
      
    ELSE
        new.title_eng :=
            setweight(
                to_tsvector(
                    'pg_catalog.english',
                    coalesce(
                        regexp_replace(new.title, '[^[:alnum:]]', ' ', 'g'),
                    '')
                ),
                'A'
            );
    END IF;

    RETURN new;
end
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS tsvector_update_core_page ON core_page;
CREATE TRIGGER tsvector_update_core_page BEFORE INSERT OR UPDATE
    ON core_page FOR EACH ROW EXECUTE PROCEDURE core_page_trigger();

DROP TRIGGER IF EXISTS tsvector_update_core_basetreenode ON core_page;
CREATE TRIGGER tsvector_update_core_basetreenode BEFORE INSERT OR UPDATE
    ON core_page FOR EACH ROW EXECUTE PROCEDURE core_page_trigger();


