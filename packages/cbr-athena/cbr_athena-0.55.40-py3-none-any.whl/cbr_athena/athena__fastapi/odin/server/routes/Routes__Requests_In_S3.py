from cbr_shared.aws.s3.S3__Files_Metadata                               import S3__Files_Metadata
from cbr_shared.cbr_backend.server_requests.S3_DB__Server_Requests      import S3_DB__Server_Requests
from cbr_shared.cbr_sites.CBR_Site__Shared_Objects                      import cbr_site_shared_objects
from osbot_fast_api.api.Fast_API_Routes                                 import Fast_API_Routes
from osbot_utils.context_managers.capture_duration                      import capture_duration
from osbot_utils.decorators.methods.cache_on_self                       import cache_on_self
from osbot_utils.utils.Dev import pprint

ROUTES_PATHS__REQUESTS_IN_S3 = ['/s3-db-config', '/list-folders', '/list-files', '/list-files-metadata', '/file-contents']
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
        self.add_route_get(self.file_contents      )
        return self

    def s3_db_config(self):
        return self.s3_db().json()

    def list_folders(self, parent_folder='', return_full_path=False):
        return self.s3_db().s3_folder_list(folder=parent_folder, return_full_path=return_full_path)

    def list_files(self, parent_folder='', return_full_path=False):
        return self.s3_db().s3_folder_files(folder=parent_folder, return_full_path=return_full_path)

    def list_files_metadata(self, parent_folder=''):
        with capture_duration(action_name='list_files_metadata') as duration:
            s3_files_metadata = S3__Files_Metadata(s3_db=self.s3_db(), parent_folder=parent_folder)
            files_metadata    = s3_files_metadata.load_from_l3()
        result = dict(duration      = duration.json()    ,
                      file_count    = len(files_metadata),
                      files_metadata= files_metadata     )
        return result

    def file_contents(self, file_path):
        return self.s3_db().s3_file_data(s3_key=file_path)



