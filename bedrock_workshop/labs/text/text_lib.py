import boto3

def get_text_response(input_content):
    session = boto3.Session()
    bedrock = session.client(service_name = 'bedrock-runtime')

    message = {
        'role': 'user',
        'content': [{
            'text': input_content
        }]
    }

    response = bedrock.converse(
        modelId = 'amazon.nova-pro-v1:0',
        messages = [message],
        inferenceConfig ={
            'maxTokens': 3000,
            'temperature': 0.3,
            'topP': 0.9,
            'stopSequences': []
        }
    )

    return response['output']['message']['content'][0]['text']
