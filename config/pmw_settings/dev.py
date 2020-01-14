worker_concurrency = 1
broker_url = "filesystem://"
broker_transport_options = {
    'data_folder_in': '',
    'data_folder_out': '',
    'data_folder_processed': ''
}
worker_hijack_root_logger = True
task_default_exchange = 'papermerge'
task_ignore_result = False
result_expires = 86400
result_backend = 'rpc://'
include = 'pmworker.tasks'
accept_content = ['pickle', 'json']
s3_storage = "s3:/..."
local_storage = "local:/..."
