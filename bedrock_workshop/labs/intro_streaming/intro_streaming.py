# Streaming responses rất hữu ích khi bạn muốn bắt đầu trả về nội dung ngay lập tức 
# Có thể hiển thị đầu ra một vài từ tại một thời điểm, thay vì chờ toàn bộ phản hồi được tạo
import boto3 

# Định nghĩa trình xử lí (handler) callback cho kết quả truyền trực tuyến (streaming)
## Hàm này cho phép in từng phần (chunks) phản hổi khi chúng được trả về từ streaming API
def chunk_handler(chunk):
    print(chunk, end='')

# Xác định function để gọi AB streaming API
## Sử dụng chức năng AB's 'converse_stream' để gọi đến streaming API endpoint
## Khi các phần response được trả về, code này sẽ trích xuất (extract) văn bản của phần đó từ JSON nhận được và chuyển nó đến 
## hàm callback được cung cấp

def get_streaming_response(prompt, streaming_callback):
    session = boto3.Session()
    bedrock = session.client(service_name = 'bedrock-runtime')

    message = {
        'role': 'user',
        'content': [{
            'text': prompt
        }]
    }

    response = bedrock.converse_stream(
        modelId = 'anthropic.claude-3-sonnet-20240229-v1:0',
        messages = [message], #luôn luôn đặt trong một list REMEMBER
        inferenceConfig = {
            'maxTokens': 2000,
            'temperature': 0
        }
    )

    stream = response.get('stream')
    for event in stream:
        if 'contentBlockDelta' in event:
            streaming_callback(event['contentBlockDelta']['delta']['text'])

prompt = 'Hãy mô tả cho tôi về chó phú quốc ?'

get_streaming_response(prompt,chunk_handler)

print('\n')