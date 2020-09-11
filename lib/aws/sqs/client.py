import boto3


class SQSClient(object):
    def __init__(self):
        self.client = boto3.client('sqs')

    def send_message(self, queue_url: str, body: str):
        self.client.send_message(QueueUrl=queue_url, MessageBody=body)

    def get_queue_url(self, queue_name: str) -> str:
        return self.client\
                   .get_queue_url(QueueName=queue_name)\
                   .get("QueueUrl")
