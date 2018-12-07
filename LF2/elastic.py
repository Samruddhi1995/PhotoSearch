import boto3
import json
import requests
from requests_aws4auth import AWS4Auth


def elastic(keywordone, keywordtwo):
    print("elastic module was called")
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = 'https://vpc-my-search-domain-2vwmgvgyecvhk7zkvvhx3ovrqa.us-east-1.es.amazonaws.com'  # the Amazon ES domain, including https://
    index = 'searchphoto'
    type = '_doc'

    url = host + '/' + index + '/_search'
    print(url)
    # Lambda execution starts here
    print(keywordtwo)
    print(keywordone)
    if keywordtwo == None:
        query = {
            "query": {
                "match": {
                    "labels": keywordone
                }
            }
        }
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    else:

        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "labels": keywordone
                            }
                        },
                        {
                            "match": {
                                "labels": keywordtwo
                            }
                        }
                    ]
                }
            }
        }

    print(query)

    # ES 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    data = (r.json())
    print("data")
    print(json.dumps(data))
    n = data["hits"]["total"]
    n = int(n)
    if n == 0:
        print("N is zero")
        return ("No such search results!")
    else:

        print(n)
        Photo = [dict() for x in range(n)]
        for i in range(n):
            bucket = data["hits"]["hits"][i]["_source"]['bucket']
            objectKey = data["hits"]["hits"][i]["_source"]['objectKey']
            labels = data["hits"]["hits"][i]["_source"]['labels']
            url = "https://s3.amazonaws.com/" + bucket + "/" + objectKey
            Photo[i]['url'] = url
            Photo[i]['labels'] = labels
        SearchResponse = {}
        SearchResponse['results'] = Photo
        print(json.dumps(SearchResponse))
        return (json.dumps(SearchResponse))

