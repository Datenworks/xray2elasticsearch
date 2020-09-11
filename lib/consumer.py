from lib import log
from lib.aws.sqs.event import AwsSqsEvent
from lib.aws.sqs.event_record import AwsSqsEventRecord
import json


class ConsumerInputParser(object):
    def __init__(self, input_data):
        self.input_data = input_data

    def iterator(self):
        log('Parsing inputs')
        sqs_event = AwsSqsEvent(event=self.input_data)
        for record in sqs_event.each_record():
            sqs_record = AwsSqsEventRecord(record)
            body = json.loads(sqs_record.get_body())
            yield body
