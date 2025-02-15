import boto3
import json

print ("\n---- A basic call to the Converse API")

session = boto3.Session()
bedrock = session.client(service_name="bedrock-runtime")

s3 = session.client(service_name="s3")
bucket = "backend-s3-bedrock"
key = "beckrock_workshop/labs/image_search/images/z1001.jpg"

message_list = []

print("\n----Alternating user and assistant messages----\n")

initial_message = {
    "role": "user",
    "content": [
        {
            "text": "Who are you ?"
        }
    ],
}

message_list.append(initial_message)

response = bedrock.converse(
    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages = message_list,
    inferenceConfig = {
        "maxTokens": 2000,
        "temperature": 0.5,
    },
)

response_message = response["output"]["message"]
print(json.dumps(response_message, indent=4))



print("\n----Including an image in a message----\n")

response = s3.get_object(Bucket=bucket, Key=key)
image_bytes = response['Body'].read()

# with open("image.webp", "rb") as image_file:
#     image_bytes = image_file.read()

image_message = {
    "role": "user",
    "content": [
        { "text": "Image 1:" },
        {
            "image": {
                "format": "jpeg",
                "source": {
                    "bytes": image_bytes
                }
            }
        },
        { "text": "Please describe the image." }
    ],
}

message_list.append(image_message)

response = bedrock.converse(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    messages=message_list,
    inferenceConfig={
        "maxTokens": 2000,
        "temperature": 0
    },
)

response_message = response['output']['message']
print(json.dumps(response_message, indent=4))

message_list.append(response_message)


print("\n----Setting a system prompt----\n")
summary_message = {
    "role": "user",
    "content": [
        {
            "text": "Can you sumarrize our conversation so far ?"
        }
    ],
}

message_list.append(summary_message)
response = bedrock.converse(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    messages=message_list,
    system=[
        {
            "text": "Please respond to all request in the style of a Customer Service Representative"
        }
    ],
    inferenceConfig={
        "maxTokens": 2000,
        "temperature": 0
    },
)

response_message = response['output']['message']
print(json.dumps(response_message, indent=4))

message_list.append(response_message)

# The "stopReason" property tells us why the model completed the message. 
# This can be useful for your application logic, error handling, or troubleshooting.

# The "usage" property includes details about the input and output tokens. 
# This can help you understand the charges for your API call.

print("\n----Getting response metadata and token counts----\n")
print("Stop reason: ", response["stopReason"])
print("Usage: ", json.dumps(response["usage"], indent=4)) #json.dumps is used to pretty print the JSON object