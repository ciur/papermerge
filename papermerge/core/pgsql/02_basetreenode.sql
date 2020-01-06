--SET search_path TO eugen,public;

/****
ancestors_to_tsvector(arr_ancestors text[]) RETURNS tsvector

Builds and assign weights from array of ancestors.
**/
CREATE OR REPLACE FUNCTION ancestors_to_tsvector(
    config regconfig,
    arr_ancestors text[]
) RETURNS tsvector AS $$
    DECLARE
        ts_ancestors tsvector := '{}';
        title text;
        clean_title text; -- title only with alphanum chars separated by one space.
    BEGIN
      FOREACH title IN ARRAY arr_ancestors LOOP
	    -- remove all non alphanumeric tiles from title, like ",_-;-" etc.
		-- leave just spaces instead.
        clean_title := regexp_replace(title, '[^[:alnum:]]', ' ', 'g');	
      
		ts_ancestors := setweight(
			to_tsvector(config, clean_title), 'B'
		) || ts_ancestors;
      END LOOP;
      
      RETURN ts_ancestors;
    END;
$$ LANGUAGE plpgsql;


/****
get_ancestors(node_id integer) RETURNS text[]

Returns an array of titles of ancestors of node_id
(like a breadcrumb in webapp).

The closest ancestor will be on the right end of array.
Given following structure:

Folder_1  
   |
Folder_11
  / \
 /   \
FX   FY
      |
    document.pdf <- with doc_id as id.
    
get_ancestors(doc_id) will return:

{Folder_1, Folder_11, FY}
***/
CREATE OR REPLACE  FUNCTION get_ancestors(
    node_id integer
) RETURNS text[] AS $$
    DECLARE
        parents_arr text[] := '{}';
        current_id integer;
        node RECORD;
    BEGIN
        current_id := node_id;
        LOOP

			SELECT basetree.*, ctype.model AS model_type
			INTO node
            FROM core_basetreenode basetree
			LEFT OUTER JOIN django_content_type ctype ON (basetree.polymorphic_ctype_id = ctype.id)
	        WHERE basetree.id = current_id;

            IF node.model_type = 'document' AND node.id <> node_id 
            THEN
                -- documents will not include self in ancestors list
                parents_arr :=  node.title::text || parents_arr;
			ELSIF node.model_type = 'folder'
			THEN
				-- folders will include self in ancestors list
				parents_arr :=  node.title::text || parents_arr;
            END IF;
            
            IF node.parent_id is NULL
            THEN
                RETURN parents_arr; -- exit loop on first null parent.
            END IF;

            current_id := node.parent_id;
        END LOOP;
    END;

$$ LANGUAGE plpgsql;


--SELECT node.tree_id,
--        node.title,
--        ctype.model,
--		get_ancestors(node.id),
--        ancestors_to_tsvector(
--        'german',
--        get_ancestors(node.id)
--       ) as ts_ancestors
--FROM core_basetreenode as node
--LEFT OUTER JOIN django_content_type ctype ON (node.polymorphic_ctype_id = ctype.id)
--ORDER BY node.tree_id;


