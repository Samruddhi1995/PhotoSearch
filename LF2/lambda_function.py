import json
import boto3
import elastic

def lambda_handler(event, context):
    # extracting querry
    print(json.dumps(event))
    query = event["queryStringParameters"]['q']
    # print(query)

    # sending query to lex to extract keywords
    response = calling_lex(query)
    return {
        "statusCode": 200,
        "body": response,
        "headers": {
            "Access-Control-Allow-Origin": "*"}
    }


def calling_lex(query):
    client = boto3.client('lex-runtime')
    response = client.post_text(botName='SearchIntent', botAlias='$LATEST', userId='USER', inputText=query)

    print(json.dumps(response))
    if response['dialogState'] == "ReadyForFulfillment":
        keywordone = response['slots']['keywordone']
        keywordtwo = response['slots']['keywordtwo']

        print(keywordone)
        print(keywordtwo)
        response = elastic.elastic(keywordone, keywordtwo)
        print("response from elastic module")
        print(response)
    else:
        response = "Inappropiate Querry"

    return response