import json
from datetime import datetime


class XrayTrace(object):
    def __init__(self, trace: str):
        self.trace = self.__parse_trace_documents(trace=trace)

    def trace_as_dict(self) -> dict:
        return self.trace

    def newest_segment_datetime(self) -> datetime:
        newest_segment_datetime = None
        for segment in self.trace.get('Segments', dict()):
            start_timestamp = segment.get("Document", dict())\
                                     .get("start_time", 0)
            segment_datetime = datetime.fromtimestamp(start_timestamp)
            if newest_segment_datetime is None or \
               segment_datetime > newest_segment_datetime:
                newest_segment_datetime = segment_datetime
        return newest_segment_datetime

    def __parse_trace_documents(self, trace: str) -> dict:
        parsed_trace = trace
        parsed_segments = []
        for segment in trace.get("Segments", list(dict())):
            parsed_segment = segment
            parsed_segment.update(
                {
                    "Document": json.loads(parsed_segment.get("Document"))
                }
            )
            parsed_segments.append(parsed_segment)
        parsed_trace.update({"Segments": parsed_segments})
        return parsed_trace
