from cbr_shared.cbr_backend.server_requests.S3_DB__Server_Requests import S3_DB__Server_Requests
from cbr_shared.cbr_sites.CBR_Site__Shared_Objects  import cbr_site_shared_objects
from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from osbot_utils.context_managers.capture_duration import print_duration, capture_duration
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_name

ROUTES_PATHS__REQUESTS_IN_S3 = ['/s3-db-config', '/list-folders', '/list-files', '/list-files-metadata']
ROUTE_PATH__REQUESTS_IN_S3   = 'requests-in-s3'

class Routes__Requests_In_S3(Fast_API_Routes):
    tag                   : str = ROUTE_PATH__REQUESTS_IN_S3
    s3_db_server_requests : S3_DB__Server_Requests              = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cache_on_self
    def s3_db(self):
        return cbr_site_shared_objects.s3_db_server_requests()                                  # this will create a bucket if it doesn't exist

    def setup_routes(self):
        self.add_route_get(self.s3_db_config       )
        self.add_route_get(self.list_folders       )
        self.add_route_get(self.list_files         )
        self.add_route_get(self.list_files_metadata)
        return self

    def s3_db_config(self):
        return self.s3_db().json()

    def list_folders(self, parent_folder='', return_full_path=False):
        return self.s3_db().s3_folder_list(folder=parent_folder, return_full_path=return_full_path)

    def list_files(self, parent_folder='', return_full_path=False):
        return self.s3_db().s3_folder_files(folder=parent_folder, return_full_path=return_full_path)

    def list_files_metadata(self, parent_folder=''):
        files_paths    = self.s3_db().s3_folder_files(folder=parent_folder, return_full_path=True)
        files_metadata = []
        s3_bucket      = self.s3_db().s3_bucket()
        s3             = self.s3_db().s3()
        with capture_duration(action_name='list_files_metadata') as duration:
            for file_path in files_paths:
                file_info     = s3.file_details(bucket=s3_bucket, key=file_path)
                file_metadata = dict(file_name = file_name(file_path,check_if_exists=False),
                                     metadata  = file_info.get('Metadata'),
                                     length    = file_info.get('ContentLength'))
                files_metadata.append(file_metadata)

        result = dict(duration       = duration.json()  ,
                      files_metadata = files_metadata)
        return result

