import boto3
import json

session = boto3.Session()
bedrock = session.client(service_name="bedrock-runtime") #create a bedrock client 

bedrock_model_id = "amazon.titan-text-express-v1" #set the foundation model

prompt = "50 + 1 bằng bao nhiêu ?" #the prompt to send to the model

body = json.dumps({
    "inputText": prompt,
    "textGenerationConfig": {
        "temperature": 0,  
        "topP": 0.5,
        "maxTokenCount": 1024,
        "stopSequences": []
    }
}) #build the request payload

#Call the amazon bedrock API: use Bedrock's invoke_model function to make the call.

response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') #send the payload to Amazon Bedrock

# Display the response: This extracts & prints the returned text from the model's response JSON.
response_body = json.loads(response.get("body").read()) # read the response
response_text = response_body["results"][0]["outputText"] #extract the text from JSON response

print(response_text)
