CREATE OR REPLACE FUNCTION public.dgl_delete_customer(customer_name text) RETURNS void AS $$
BEGIN
    DELETE FROM public.customers_domain
    WHERE tenant_id IN (
        SELECT id 
        FROM public.customers_client
        WHERE name = customer_name
    );
    DELETE FROM public.customers_client
    WHERE name = customer_name;
    
    EXECUTE 'DROP SCHEMA ' || customer_name || ' CASCADE'; 
END
$$ LANGUAGE PLPGSQL;


DROP VIEW IF EXISTS customers;
CREATE OR REPLACE VIEW customers AS
SELECT client.id,
    client.schema_name,
    client.name,
    client.email,
    dom.domain
FROM public.customers_client AS client
LEFT OUTER JOIN public.customers_domain AS dom 
ON (dom.tenant_id = client.id);