import os
import boto3
import string
import random
import json
import time

cwlogs = boto3.client('logs')


def createLogGroup(logGroupName):
    createLogGroupResponse = cwlogs.create_log_group(
        logGroupName=logGroupName,
        tags={
            "Owner": "TrendMicro",
            "Product": "CloudOneWorkloadSecurity",
            "Name": logGroupName
        }
    )

    print("createLogGroupResponse - " + str(createLogGroupResponse))


def ifLogGroupExists(logGroupName):
    listLogGroupsResponse = cwlogs.describe_log_groups()
    for logGroup in listLogGroupsResponse["logGroups"]:
        if logGroupName in logGroup["logGroupName"]:
            return True
    return False


def createLogStream(logGroupName, logStreamName):
    createLogStreamResponse = cwlogs.create_log_stream(
        logGroupName=logGroupName,
        logStreamName=logStreamName
    )

    print("createLogStreamResponse - " + str(createLogStreamResponse))

    if createLogStreamResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return logStreamName
    return ""


def putLogEvents(logGroupName, logStreamName, logEvent, nextSequenceToken=None):

    if nextSequenceToken:
        putLogEventsResponse = cwlogs.put_log_events(
            logGroupName=logGroupName,
            logStreamName=logStreamName,
            logEvents=logEvent,
            sequenceToken=nextSequenceToken
        )
    else:
        putLogEventsResponse = cwlogs.put_log_events(
            logGroupName=logGroupName,
            logStreamName=logStreamName,
            logEvents=logEvent
        )

    print("putLogEventsResponse - " + str(putLogEventsResponse))

    if "rejectedLogEventsInfo" not in putLogEventsResponse:
        return putLogEventsResponse["nextSequenceToken"]
    return None


def lambda_handler(event, context):

    nextSequenceToken = None

    logGroupName = str(os.environ.get("CloudWatchLogGroupName"))
    logStreamNamePrefix = str(os.environ.get("CloudWatchLogStreamNamePrefix"))

    nonce = ''.join(random.choices(
        string.ascii_letters + string.digits, k=8)).upper()

    logEvents = json.loads(event["Records"][0]["Sns"]["Message"])

    if len(logEvents) > 0:

        if ifLogGroupExists(logGroupName):
            logStreamName = createLogStream(
                logGroupName, logStreamNamePrefix + "-" + nonce)
        else:
            createLogGroup(logGroupName)
            logStreamName = createLogStream(
                logGroupName, logStreamNamePrefix + "-" + nonce)

        print(str(logGroupName) + " - " + str(logStreamName))

        for message in logEvents:

            epoch_time = int(round(time.time() * 1000))

            logEvent = []
            logEvent.append({"timestamp": epoch_time, "message": str(message)})

            nextSequenceToken = putLogEvents(
                logGroupName, logStreamName, logEvent, nextSequenceToken)

            if nextSequenceToken == None:
                return False
