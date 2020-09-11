try:
  import unzip_requirements
except ImportError:
  pass

import json
from lib.aws.xray.client import XrayClient
from lib.aws.xray.trace import XrayTrace
from os import getenv
from datetime import datetime, timedelta
from lib.aws.sqs.client import SQSClient
from lib.aws.ssm.parameter_store import AwsParameterStoreClient
from lib import log

SQS_QUEUE_NAME = getenv("SQS_QUEUE_NAME")
SSM_PARAMETER_NAME = getenv("SSM_PARAMETER_NAME",
                            "xray-consumer-last-segment-datetime")


def execute(event, context):
    xray_client = XrayClient()
    sqs_client = SQSClient()
    paramters_client = AwsParameterStoreClient()

    try:
        start_raw = paramters_client.get(SSM_PARAMETER_NAME)
    except Exception:
        start_raw = (datetime.now() - timedelta(hours=2)).isoformat()

    start_datetime = datetime.fromisoformat(start_raw)
    end_datetime = datetime.now()

    newest_trace_datetime = None
    newest_segment_datetime = None
    log(f"Collecting between {start_datetime} and {end_datetime}")
    for trace_id in xray_client.trace_ids_iterator(start=start_datetime,
                                                   end=end_datetime):
        traces = xray_client.trace_by_id(trace_id)['Traces']
        log(f"Collecting {len(traces)} traces")
        for trace in traces:
            log("Parsing trace")
            xray_trace = XrayTrace(trace=trace)
            parsed_trace = xray_trace.trace_as_dict()

            log("Checking segments start_time")
            newest_segment_datetime = xray_trace.newest_segment_datetime()
            if newest_trace_datetime is None or \
               newest_segment_datetime > newest_trace_datetime:
                log(f"Old newest_trace_datetime {newest_trace_datetime}")
                log(f"Actual newest_trace_datetime {newest_segment_datetime}")
                newest_trace_datetime = newest_segment_datetime

            log("Sending trace to SQS")
            queue_url = sqs_client.get_queue_url(SQS_QUEUE_NAME)
            sqs_client.send_message(
                queue_url=queue_url, body=json.dumps(parsed_trace))

    if newest_segment_datetime:
      log("Saving the max_datetime into parameters store")
      paramters_client.put(name=SSM_PARAMETER_NAME,
                          value=newest_segment_datetime.isoformat())
