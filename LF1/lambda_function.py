from __future__ import print_function
import boto3
import re
from decimal import Decimal
import json
import urllib
import requests
from requests_aws4auth import AWS4Auth

rekognition = boto3.client('rekognition')




#indexing json in Elastic search
def elastic_put(document):

    region = 'us-east-1'  # e.g. us-west-1
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = 'https://vpc-my-search-domain-2vwmgvgyecvhk7zkvvhx3ovrqa.us-east-1.es.amazonaws.com'  # the Amazon ES domain, including https://
    index = 'searchphoto'
    type = '_doc'
    url = host + '/' + index + '/' + type

    headers = {"Content-Type": "application/json"}
    #print("Hey")

    r = requests.post(url, auth=awsauth, json=document, headers=headers)
    print("This response from Elastic Search")
    print(r)
    return




# --------------- Helper Functions to call Rekognition APIs ------------------
def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    # table = boto3.resource('dynamodb').Table('MyTable')
    # labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    labelsArray = [str(label_prediction['Name']) for label_prediction in response['Labels']]
    print("List of lables")
    print(labelsArray)
    # table.put_item(Item={'PK': key, 'Labels': labels})
    return labelsArray


# --------------- Main handler ------------------
def lambda_handler(event, context):
    print(json.dumps(event))
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    createdTimestamp = event['Records'][0]['eventTime']
    #print(createdTimestamp)
    bucket = event['Records'][0]['s3']['bucket']['name']
    #print(bucket)
    objectKey = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    #print(objectKey)
    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
        # response = detect_faces(bucket, key)

        # Calls rekognition DetectLabels API to detect labels in S3 object
        labelsArray = detect_labels(bucket, objectKey)
        # JSON DOCUMENT
        document = {"objectKey": objectKey, "bucket": bucket, "createdTimestamp": createdTimestamp,
                    "labels": labelsArray}

        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        # response = index_faces(bucket, key)

        # Print response to console.
        print(json.dumps(document))

        elastic_put(document)
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(objectKey, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
