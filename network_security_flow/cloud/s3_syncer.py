import os 

class S3Sync:
    def sync_folder_to_s3(self,folder,s3_bucket_url):
            cmnd = f'aws s3 sync {folder} {s3_bucket_url}'
            os.system(cmnd)
    
    def sync_folder_from_s3(self,folder,s3_bucket_url):
          cmnd = f'aws s3 sync {s3_bucket_url} {folder}'
          os.system(cmnd)