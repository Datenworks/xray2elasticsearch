import boto3


class AwsParameterStoreClient(object):
    def __init__(self):
        self.client = boto3.client('ssm')

    def get(self, name: str):
        return self.client\
                   .get_paramter(Names=name)\
                   .get("Parameter")\
                   .get("Value")

    def put(self, name, value: str, value_type: str = "String"):
        return self.client\
                   .put_parameter(Name=name,
                                  Type=value_type,
                                  Value=value,
                                  Overwrite=True)
