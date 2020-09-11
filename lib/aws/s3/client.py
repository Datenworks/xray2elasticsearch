import boto3

from urllib.parse import unquote


class AwsS3Client(object):

    def __init__(self, region: str = 'us-east-1'):
        self.s3 = boto3.client('s3', region_name=region)

    def put_object(self, bucket: str, file_path: str, data: str):
        return self.s3.put_object(Bucket=bucket, Key=file_path, Body=data)

    def get_object(self, bucket: str, file_path: str) -> dict:
        return self.s3.get_object(Bucket=bucket,
                                  Key=file_path)

    def download_object(self, bucket: str,
                        file_path: str,
                        local_path: str) -> dict:
        return self.s3.download_file(Bucket=bucket,
                                     Key=file_path,
                                     Filename=local_path)

    def list_bucket(self, bucket: str, path: str) -> dict:
        return self.s3.list_objects_v2(Bucket=bucket,
                                       Prefix=f"{path}/_metadata")

    def read_object_content(self, bucket: str, file_path: str) -> dict:
        response = self.s3.get_object(Bucket=bucket,
                                      Key=unquote(file_path))
        file_stream = response['Body']
        body = file_stream.read().decode()
        return body

    def file_exists(self, bucket: str, file_path: str) -> bool:
        response = self.list_bucket(bucket, file_path)
        return response.get('KeyCount', 0) > 0
