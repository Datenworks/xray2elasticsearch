class AwsSqsEventRecord(object):

    def __init__(self, event: dict):
        self.event = event

    def get_body(self):
        return self.event['body']
