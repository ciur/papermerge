-- Following ON DELETE CASCADE constraints will make sure that
-- simple command:
--
-- DELETE FROM auth_user WHERE id = <user_id>
-- will delete all data related to <user_id>.
-- 
-- You want deleteing user with a simple command, right?
-- But you don't want unused IDs to stay arround.

ALTER TABLE core_userprofile
DROP CONSTRAINT core_userprofile_user_id_5141ad90_fk_auth_user_id,
ADD CONSTRAINT core_userprofile_user_id_5141ad90_fk_auth_user_id
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE core_page
DROP CONSTRAINT core_page_user_id_6a42c58e_fk_auth_user_id,
ADD CONSTRAINT core_page_user_id_6a42c58e_fk_auth_user_id
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE core_basetreenode
DROP CONSTRAINT core_basetreenode_user_id_cb6e3a29_fk_auth_user_id,
ADD CONSTRAINT core_basetreenode_user_id_cb6e3a29_fk_auth_user_id
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE auth_user_groups
DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id,
ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE auth_user_user_permissions
DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id,
ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE django_admin_log
DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id,
ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE dynamic_preferences_users_userpreferencemodel
DROP CONSTRAINT dynamic_preferences__instance_id_bf1d7718_fk_auth_user,
ADD CONSTRAINT dynamic_preferences__instance_id_bf1d7718_fk_auth_user
    FOREIGN KEY (instance_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE core_folder
DROP CONSTRAINT core_folder_basetreenode_ptr_id_40711dcc_fk_core_base,
ADD CONSTRAINT core_folder_basetreenode_ptr_id_40711dcc_fk_core_base
    FOREIGN KEY (basetreenode_ptr_id)
    REFERENCES core_basetreenode(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE core_document
DROP CONSTRAINT core_document_basetreenode_ptr_id_b4782aec_fk_core_base,
ADD CONSTRAINT core_document_basetreenode_ptr_id_b4782aec_fk_core_base
    FOREIGN KEY (basetreenode_ptr_id)
    REFERENCES core_basetreenode(id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE core_page
DROP CONSTRAINT core_page_document_id_183b2acc_fk_core_docu,
ADD CONSTRAINT core_page_document_id_183b2acc_fk_core_docu
    FOREIGN KEY (document_id)
    REFERENCES core_document(basetreenode_ptr_id)
    ON DELETE CASCADE
    DEFERRABLE INITIALLY DEFERRED;










    