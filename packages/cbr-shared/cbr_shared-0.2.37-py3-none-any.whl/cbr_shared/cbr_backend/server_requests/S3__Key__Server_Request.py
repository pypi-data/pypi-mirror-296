from datetime                           import datetime, timezone
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc import random_guid, utc_now

S3_PATH__WHEN_BLOCK_SIZE   = 5

class S3__Key__Server_Request(Type_Safe):
    root_folder       : str  = None
    server_name       : str  = None
    use_when          : bool = True
    use_date          : bool = True
    use_hours         : bool = True
    use_minutes       : bool = True
    use_request_path  : bool = False
    save_as_gz        : bool = False
    s3_path_block_size: int = S3_PATH__WHEN_BLOCK_SIZE

    def create(self, when=None, what=None, request_id=None, request_path=None):
        if when is None:
           when = self.path__for_date_time__now_utc()
        if what is None:                                            # todo: to implement
            pass
        if not request_id:
            request_id = random_guid()
        path_elements = []
        if self.root_folder     : path_elements.append(self.root_folder )
        if self.server_name     : path_elements.append(self.server_name )
        if what                 : path_elements.append(what             )
        if self.use_when:
            if when             : path_elements.append(when             )
        if self.use_request_path:
            if request_path:
                if request_path == '/':
                    request_path = '(root)'                                      # todo: see implications of this (since boto3 on AWS handles this ok, but minio doesn't like a / as the path
                else:
                    request_path = request_path[1:]
                if request_path:
                    path_elements.append(request_path)
        if request_id           : path_elements.append(request_id       )

        s3_key = '/'.join(path_elements) + '.json'
        if self.save_as_gz:
            s3_key += ".gz"
        return s3_key

    def path__for_date_time__now_utc(self):
        return self.path__for_date_time(utc_now())

    def path__for_date_time(self, date_time):
        minute       = date_time.minute
        date_path    = date_time.strftime('%Y-%m-%d')                          # Format the date as YYYY-MM-DD
        hour_path    = date_time.strftime('%H')                                # Format the hour
        minute_block = self.calculate_minute_block(minute)
        path_components = []
        if self.use_date:
            path_components.append(date_path   )
        if self.use_hours:
            path_components.append(hour_path   )
        if self.use_minutes:
            path_components.append(minute_block)
        s3_path = '/'.join(path_components)
        return s3_path

    def calculate_minute_block(self, minute):
        block_size   = self.s3_path_block_size                                  # get the block size in minutes (configurable)
        minute_block = f"{(int(minute) // block_size) * block_size:02d}"        # Calculate the block using the configurable block size
        return minute_block