import json 
import boto3

session = boto3.Session()
bedrock = session.client(service_name = "bedrock-runtime")

message_list = []

s3 = session.client('s3')
bucket = "backend-s3-bedrock"
key = "beckrock_workshop/labs/image_search/images/z1002.jpg"

response = s3.get_object(Bucket=bucket, Key=key)
image_bytes = response['Body'].read()


image_message = {
    "role": "user",
    "content": [
        {
            "text": "Image1"
        },
        {
            "image": {
                "format": "jpeg",
                "source": {
                    "bytes": image_bytes
                }
            }
        },
        {
            "text": "please describe the image"
        }
    ],
}

message_list.append(image_message)
response = bedrock.converse(
    modelId = "anthropic.claude-3-sonnet-20240229-v1:0",
    messages = message_list,
    inferenceConfig={
        "maxTokens": 2000,
        "temperature": 0
    },
)

response_message = response["output"]["message"]
print(json.dumps(response_message, indent = 4))
message_list.append(response_message)