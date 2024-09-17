from cbr_shared.cbr_backend.server_requests.S3_DB__Server_Requests   import S3_DB__Server_Requests
from osbot_fast_api.api.Fast_API__Request_Data                       import Fast_API__Request_Data
from osbot_utils.base_classes.Type_Safe                              import Type_Safe
from osbot_utils.helpers.Random_Guid                                 import Random_Guid
from osbot_utils.utils.Misc                                          import timestamp_to_str_time


class S3__Server_Request(Type_Safe):
    s3_db        : S3_DB__Server_Requests
    what         : str                      = None
    when         : str                      = None
    request_id   : Random_Guid
    request_data : Fast_API__Request_Data   = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.request_data:
            self.request_id = self.request_data.request_id

    def create(self):
        if self.request_data:
            s3_key    = self.s3_key()
            data      = self.request_data.json()
            metadata  = dict(s3_key       = s3_key                                            ,
                             request_path = self.request_data.request_path                    ,
                             status_code  = str(self.request_data.response_status_code       ),
                             timestamp    = str(self.request_data.timestamp                  ),
                             time         = timestamp_to_str_time(self.request_data.timestamp),
                             duration     = str(self.request_data.request_duration           ),
                             content_size = str(self.request_data.response_content_length    ),
                             method       = self.request_data.request_method                  )
            return self.s3_db.s3_save_data(data=data, s3_key=s3_key, metadata=metadata)

    def create_from_request_data(self, request_data: Fast_API__Request_Data):
        self.request_data = request_data
        self.request_id   = request_data.request_id
        return self.create()

    def delete(self):
        return self.s3_db.s3_file_delete(self.s3_key())

    def exists(self):
        return self.s3_db.s3_file_exists(self.s3_key())

    def metadata(self):
        return self.s3_db.s3_file_metadata(self.s3_key())

    def load(self, s3_key):
        raw_data          = self.s3_db.s3_file_data(s3_key)       # we can't use self.s3_key()  since there are scenarios where data from request_data is needed
        if raw_data:
            self.request_data = Fast_API__Request_Data.from_json(raw_data)
            self.request_id   = self.request_data.request_id
        return self



    def s3_key(self):
        kwargs = dict(what         = self.what          ,
                      when         = self.when          ,
                      request_id   = self.request_id    ,
                      request_path = self.request_path())
        return self.s3_db.s3_key(**kwargs)

    def request_path(self):
        if self.request_data:
            return self.request_data.request_path


