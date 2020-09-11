import boto3
from datetime import datetime, timedelta
from lib import log


class XrayClient(object):
    def __init__(self):
        self.client = boto3.client('xray')

    def get_trace_summaries(self,
                            start: datetime,
                            end: datetime,
                            filter_expression: str = 'ok or !ok',
                            next_token: str = ''):
        return self.client\
                   .get_trace_summaries(StartTime=start,
                                        EndTime=end,
                                        FilterExpression=filter_expression,
                                        NextToken=next_token)

    def batch_get_traces(self, trace_ids: list):
        return self.client.batch_get_traces(TraceIds=trace_ids)

    def trace_by_id(self, trace_id: str):
        return self.batch_get_traces(trace_ids=[trace_id])

    def trace_ids_iterator(self,
                           start: datetime,
                           end: datetime,
                           filter_expr: str = 'ok or !ok'):

        if not self.__less_than_24_hours(start, end):
            end = start + timedelta(seconds=23*60*60)

        response = self.get_trace_summaries(start=start,
                                            end=end,
                                            filter_expression=filter_expr)
        next_token = response.get('NextToken', None)
        while True:
            summaries = response["TraceSummaries"]
            log(f"Fetching {len(summaries)} trace summaries IDs")
            for summary in summaries:
                yield summary['Id']

            if next_token is None:
                break
            summaries = self.get_trace_summaries(start=start,
                                                 end=end,
                                                 filter_expression=filter_expr,
                                                 next_token=next_token)
            next_token = summaries.get('NextToken', None)

    def __less_than_24_hours(self, start, end):
        difference = end - start
        return difference.total_seconds() < 24 * 60 * 60
