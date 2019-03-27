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
    def post(self, path_parameter_in_uri):

        #Create SQS client and login 
        # DO NOT CHECK IN WITH CREDENTIALS
        sqs = boto3.client('sqs', region_name='us-east-1',
            aws_access_key_id='YOUR_KEY_HERE',
            aws_secret_access_key='_YOUR_KEY_HERE'
            )
        queue_url = 'YOUR_QUEUE_HERE'

        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'Example': {
                    'DataType': 'String',
                    'StringValue': 'This is some message attribute'
                },
                'Another_Example': {
                    'DataType': 'String',
                    'StringValue': 'This is another attribute'
                }
            },
            # Pass the path parameter that was sent in as the message body
            MessageBody=(path_parameter_in_uri)
        )
        print(response['MessageId'])
        return response['MessageId'], 201

