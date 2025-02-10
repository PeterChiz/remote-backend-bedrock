import boto3
import json

print ("\n---- A basic call to the Converse API")

session = boto3.Session()
bedrock = session.client(service_name="bedrock-runtime")

message_list = []

# print("\n----Alternating user and assistant messages----\n")

# initial_message = {
#     "role": "user",
#     "content": [
#         {
#             "text": "Who are you ?"
#         }
#     ],
# }

# message_list.append(initial_message)

# response = bedrock.converse(
#     modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0",
#     messages = message_list,
#     inferenceConfig = {
#         "maxTokens": 2000,
#         "temperature": 0.5,
#     },
# )

# response_message = response["output"]["message"]
# print(json.dumps(response_message, indent=4))

print("\n----Including an image in a message----\n")

with open("image.webp", "rb") as image_file:
    image_bytes = image_file.read()

image_message = {
    "role": "user",
    "content": [
        { "text": "Image 1:" },
        {
            "image": {
                "format": "webp",
                "source": {
                    "bytes": image_bytes #no base64 encoding required!
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

