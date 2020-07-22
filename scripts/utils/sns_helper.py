import zlib
import base64


def compress_msg(msg):
    compressed = zlib.compress(msg.encode('UTF-8'))
    encoded = base64.b64encode(compressed)
    return encoded.decode('UTF-8')


def send_to_sns(sns_client, msg, topic_arn):
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=msg,
        Subject='PerformanceTest'
    )
    return response['ResponseMetadata']['HTTPStatusCode']
