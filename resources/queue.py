import boto3

# The resource file should only service the API.  The model shou;d
# handle all lifting associated to the underlying resource

# Import for resource creation and for a request parser 
from flask_restful import Resource, reqparse

class Queue(Resource):
    # Create a class-wide request parser
    parser = reqparse.RequestParser()
    # Specify which fields are being sent in the body of the request and if they are required
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # Each method corresponds to an HTTP verb corresponding to the call
    # This is what flask_restful provides
    def post(self, messagebody):

        #Create SQS client
        sqs = boto3.client('sqs', region: 'us-east-1')
        queue_url = 'https://sqs.us-east-1.amazonaws.com/846012508269/microservice_sample_queue'

        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'The Whistler'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'John Grisham'
                },
                'WeeksOn': {
                    'DataType': 'Number',
                    'StringValue': '6'
                }
            },
            MessageBody=(
                'Information about current NY Times fiction bestseller for '
                'week of 12/11/2016.'
            )
        )
        print(response['MessageId'])
        return response['MessageId'], 201

