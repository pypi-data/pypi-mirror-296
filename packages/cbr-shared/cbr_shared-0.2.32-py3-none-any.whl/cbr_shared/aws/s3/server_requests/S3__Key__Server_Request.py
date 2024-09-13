from datetime                           import datetime, timezone
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc             import random_guid

S3_PATH__WHEN_BLOCK_SIZE   = 5

class S3__Key__Server_Request(Type_Safe):
    root_folder       : str  = None
    server_name       : str  = None
    #what              : str  = None
    #when              : str  = None
    #request_id        : str  = None
    use_when          : bool = True
    use_request_path  : bool = False
    save_as_gz        : bool = False
    s3_path_block_size: int = S3_PATH__WHEN_BLOCK_SIZE

    def create(self, when=None, what=None, request_id=None, request_path=None):
        if when is None:
           when = self.s3_path__for_when()
        if what is None:                            # todo: to implement
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
                #safe_request_path = str_safe(request_path)
                path_elements.append(request_path[1:])
        if request_id           : path_elements.append(request_id       )

        s3_key = '/'.join(path_elements) + '.json'
        if self.save_as_gz:
            s3_key += ".gz"
        return s3_key

    def s3_path__for_when(self):
        now          = datetime.now(timezone.utc)                        # Generate the current date and time in UTC
        date_path    = now.strftime('%Y-%m-%d')                          # Format the date as YYYY-MM-DD
        hour_path    = now.strftime('%H')                                # Format the hour
        block_size   = self.s3_path_block_size                           # get the block size in minutes (configurable)
        minute_block = f"{(now.minute // block_size) * block_size:02d}"  # Calculate the block using the configurable block size
        s3_path      = f"{date_path}/{hour_path}/{minute_block}"
        return s3_path