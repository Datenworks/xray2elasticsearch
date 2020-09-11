.PHONY: deploy

ES_HOST := ${ES_HOST}
ES_INDEX := ${ES_INDEX}
DEPLOYMENT_BUCKET := ${DEPLOYMENT_BUCKET}
SQS_QUEUE_NAME ?= ${SQS_QUEUE_NAME}:-'xray-to-elasticsearch-delivery'
SQS_QUEUE_URL := $$(aws sqs create-queue --queue-name ${SQS_QUEUE_NAME} --output text)

deploy:
	export ES_HOST=${ES_HOST} \
		ES_INDEX=${ES_INDEX} \
		DEPLOYMENT_BUCKET=${DEPLOYMENT_BUCKET} \
		SQS_QUEUE_NAME=${SQS_QUEUE_NAME} \
		SQS_QUEUE_URL=${SQS_QUEUE_URL} &&\
		serverless deploy