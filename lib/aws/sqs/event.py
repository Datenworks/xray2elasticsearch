from lib import log


class AwsSqsEvent(object):
    def __init__(self, event):
        self.event = event
        self.records = event.get('Records', [])

    def each_record(self):
        log(f'Reading {len(self.records)} messages')
        for record in self.records:
            yield(record)
