from urllib.parse import unquote


class AwsS3EventRecord(object):

    def __init__(self, event: dict):
        self.event = event

    def get_bucket_name(self):
        return self.event['s3']['bucket']['name']

    def get_object_key(self):
        object_key = self.event['s3']['object']['key']
        return unquote(object_key)
