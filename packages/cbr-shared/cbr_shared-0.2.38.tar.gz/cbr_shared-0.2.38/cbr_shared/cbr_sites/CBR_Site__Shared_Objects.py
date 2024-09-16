from cbr_shared.cbr_backend.server_requests.S3_DB__Server_Requests import S3_DB__Server_Requests
from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class CBR_Site__Shared_Objects(Type_Safe):

    @cache_on_self
    def s3_db_server_requests(self):
        server_name = server_config__cbr_website.server_name()
        use_minio   = server_config__cbr_website.s3_s3_use_minio()                # setup use of minio (vs aws)
        kwargs      = dict(use_minio   = use_minio   ,
                           server_name =  server_name)
        with  S3_DB__Server_Requests(**kwargs)  as _:
            _.setup()                                                           # set up tasks, including creating target bucket if it doesn't exist
            _.s3_key__server_request.use_request_path = True
            _.s3_key__server_request.use_when         = True
            _.s3_key__server_request.use_minutes      = False
            _.s3_key__server_request.use_hours        = True
            return _

cbr_site_shared_objects = CBR_Site__Shared_Objects()