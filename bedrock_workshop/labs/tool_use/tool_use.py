'''
    this lab: đi qua một ví dụ đơn giản về cách sử dụng công cụ để minh họa cách nó active. 
    - Converse API: cung cấp một cách nhất quán để truy cập các LLMs trên AB. 
    API này hỗ trợ trao đổi tin nhắn theo lượt giữa user và Generative AI model, đồng thời cung cấp một định dạng tiêu chuẩn
    để định nghĩa công cụ cho các model hỗ trợ sử dụng công cụ (funtion calling)
    - Công dụng của Use Tool: là một khả năng cho phép LLMs yêu cầu ứng dụng gọi một hàm với các parameter do model cung cấp.
    Các hàm có sẵn và các parameter được hỗ trợ sẽ được truyền đến model cùng với prompt. 
    Note: LLMs k trực tiếp gọi hàm - nó chỉ trả về dữ liệu json và để ứng dụng gọi thực hiện phần còn lại
    - Use tool giúp chuyển đổi nội dung dạng tự do thành dữ liệu có cấu trúc, phù hợp cho tự động hóa và phân tích

    Quy trình Tool Use với AB Converse API
    1. Ứng dụng gọi truyền vào model:
        - (A) định nghĩa công cụ (tool definition)
        - (B) Một tin nhắn kích hoạt yêu cầu sử dụng công cụ
    2. Nếu yêu cầu khớp với tool definition, model sẽ tạo một request sử dụng công cụ bao gồm cả tham số cần truyền
    3. The calling application trích xuất parameter từ request của model và chuyển chúng đến hàm cục bộ tương ứng
    4. The calling application có thể sử dụng trực tiếp kết quả từ tool hoặc gửi kết quả đó trở lại model 
    để nhận phản hồi tiếp theo
    5. Model có thể:
        - Trả về phản hồi cuối cùng
        - Hoặc yêu cầu sử dụng một tool khác
'''

import boto3, json, math

session = boto3.Session()
bedrock = session.client(service_name = 'bedrock-runtime')

print('\n----Defining a tool and sending a message that will make Claude ask for tool use----\n')

tool_list = [
    {
        'toolSpec': {
            'name': 'cosine',
            'description': 'Caculate the cosine of x',
            'inputSchema': {
                'json':{
                    'type': 'object',
                    'properties': {
                        'x':{
                            'type': 'number',
                            'description': 'The number to pass to the funtion',
                        }
                    },
                    'required': ['x']
                }
            }
        }
    }
]

message_list = []

initial_message = {
    'role': 'user',
    'content':[
        {
            'text': 'What is the cosine of 7 ?'
        }
    ]
}

message_list.append(initial_message)

response = bedrock.converse(
    modelId = 'anthropic.claude-3-sonnet-20240229-v1:0',
    messages = message_list,
    inferenceConfig = {
        'maxTokens': 3000,
        'temperature': 0,
    },
    toolConfig={
        'tools': tool_list
    },
    system = [
        {
            'text': 'You must only do math by using a tool'
        }
    ]
)

response_message = response['output']['message']
print(json.dumps(response_message, indent = 4))
message_list.append(response_message)

'''
result:
    ----Defining a tool and sending a message that will make Claude ask for tool use----

{
    "role": "assistant",
    "content": [
        {
            "text": "Here is how we can calculate the cosine of 7 using the available tool:"
        },
        {
            "toolUse": {
                "toolUseId": "tooluse_bseNin7OTpKBDjDNqLcNmQ",
                "name": "cosine",
                "input": {
                    "x": 7
                }
            }
        }
    ]
}

- Trong trường hợp này, Claude cũng tạo ra một đoạn văn bản trước khi gửi yêu cầu sử dụng công cụ. 
Tuy nhiên, điều này không phải lúc nào cũng xảy ra. Đôi khi, Claude chỉ tạo ra một yêu cầu sử dụng công cụ 
mà không có bất kỳ văn bản kèm theo nào.
- Khối toolUse bao gồm một toolUseId. Có thể sử dụng toolUseId để giúp Claude liên kết yêu cầu công cụ ban đầu 
với kết quả tương ứng mà bạn gửi lại để xử lý tiếp theo.
- Khối toolUse cũng chỉ định tên công cụ cần gọi, trong trường hợp này là "cosine".
Thuộc tính input chứa cấu trúc JSON của các tham số truyền vào công cụ. Bạn có thể sử dụng trực tiếp JSON này. 
Trong trường hợp này, Claude yêu cầu ứng dụng gọi truyền hàm cosine với đối số x có giá trị 7.
'''

# now loop through the response message's content blocks. 
# use the cosine tool if requested and print any text content blocks form LLMs message

print('----\nCalling a function based on the toolUse content block----\n')

response_content_blocks = response_message['content']

for content_block in response_content_blocks:
    if 'toolUse' in content_block:
        tool_use_block = content_block['toolUse']
        tool_use_name = content_block['toolUse']['name']

        print(f'Using tool {tool_use_name}')

        if tool_use_name == 'cosine':
            tool_result_value = math.cos(tool_use_block['input']['x'])
            print(tool_result_value)

    elif 'text' in content_block:
        print(content_block['text'])


# Bây giờ lặp qua các content block từ response message và kiểm tra tool use response
# Nếu có yêu cầu tool use, gọi tool được chỉ định và truyền vào các tham số do Claude cung cấp
# Sau đó tạo một tin nhắn với toolResult content block để gửi lại Claude và nhận phản hồi cuối dùng

print('----\nPassing the tool result back to Claude----\n')

follow_up_content_blocks = []

for content_block in response_content_blocks:
    if 'toolUse' in content_block:
        tool_use_block = content_block['toolUse']
        tool_use_name = tool_use_block['name']

        if tool_use_name == 'cosine':
            tool_result_value = math.cos(tool_use_block['input']['x'])

            follow_up_content_blocks.append({
                'toolResult': {
                    'toolUseId': tool_use_block['toolUseId'],
                    'content':[
                        {
                            'json': {
                                'result': tool_result_value
                            }
                        }
                    ]
                }
            }) 

if len(follow_up_content_blocks) > 0:
    follow_up_message = {
        'role': 'user',
        'content': follow_up_content_blocks
    }

    message_list.append(follow_up_message)

    response = bedrock.converse(
        modelId = 'anthropic.claude-3-sonnet-20240229-v1:0',
        messages = message_list,
        inferenceConfig = {
            'maxTokens': 2000,
            'temperature': 0
        },
        toolConfig = {
            'tools': tool_list
        },
        system=[{
            'text': 'You must only do math by using a tool'
        }]
    )

    response_message = response['output']['message']

    message_list.append(response_message)
    print(json.dumps(message_list, indent = 4))

# Set the status attribute to error so that Claude can decide what to do next
print('\n----Error handling - letting Claude know that tool use failed\n')
del message_list[-2:]

content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)

if content_block:
    tool_use_block = content_block['toolUse']

#messages[2].content[0]
    error_tool_result = {
        'toolResult': {
            'toolUseId': tool_use_block['toolUseId'],
            'content': [{
                'text': 'invalid function: cosine'
            }],
            'status': 'error'
        }
    }

    follow_up_message = {
        'role': 'user',
        'content': [error_tool_result]
    }

    message_list.append(follow_up_message)

    response = bedrock.converse(
        modelId = 'anthropic.claude-3-sonnet-20240229-v1:0',
        messages = message_list,
        inferenceConfig = {
            'maxTokens': 2000,
            'temperature': 0,
        },
        toolConfig = {
            'tools': tool_list,
        },
        system = [{
            'text': 'You must only do math by using a tool'
        }]
    )

    response_message = response['output']['message']
    print(json.dumps(response_message, indent = 4))
    message_list.append(response_message)
