'''
    Inference Parameters được sử dụng để cấu hình behavior phản hồi của foundation model. 
    Inference Parameters thay đổi theo từng model:
    + Ở mức tối thiểu, chúng có thể sử dụng để ảnh hưởng đến mức độ biến đổi (Temperature, TopP) và độ dài token của phản hồi
    + Có thể hiểu token là một từ hoặc một phần của từ. Tỷ lệ tổng thể giữa số lượng token và số từ thay đổi tùy theo từng model
    trong bảng điều khiển Amazon Bedtrock, cùng với định nghĩa cho các parameter đó 
    Converse API cũng support parameter "additionalModelRequestFields", cho phép bạn đặt các Inference Parameter bổ sung cho một 
    model cụ thể mà tham số "inferenceConfig" tiêu chuẩn của Converse API không xử lý được.

'''
# Access command line arguments
import sys
import boto3

# Instantiating the Amazon Bedrock client, setting the model and getting the inference parameters for the model
def get_text_response(model, input_content):
    session = boto3.Session()
    bedrock = session.client(service_name = "bedrock-runtime")

    message = {
        "role": "user",
        "content": [
            {
                "text": input_content
            }
        ]
    }


    # - Hàm converse() dùng để gửi một yêu cầu trò chuyện
    # - topP hoạt động bằng cách chọn một tập hợp các từ có xác suất cao nhất sao cho tổng xác suất của chúng vượt 
    # quá một ngưỡng P (ví dụ: 0.7, 0.9). Sau đó, mô hình sẽ chỉ chọn từ từ tập hợp này.
    # - topP giúp cân bằng tính đa dạng và mạch lạc của văn bản, 
    # - Phù hợp cho các ứng dụng như viết truyện, tạo nội dung sáng tạo, hoặc trò chuyện với chatbot.
    # - topK là chọn K từ có xác suất cao nhất và sau đó chọn từ trong số K từ này.
    # - Phù hợp cho các ứng dụng như dịch máy, tóm tắt văn bản, hoặc trả lời câu hỏi.


    response = bedrock.converse(
        modelId = model,
        messages = [message],
        inferenceConfig = {
            "maxTokens": 2000,
            "temperature": 0.5,
            "topP": 0.7,
            "stopSequences": []
        }
    )

    return response['output']['message']['content'][0]['text']

# Passing in the first argument (Bedrock Model ID) and second argument (promt) form the command line
response = get_text_response(sys.argv[1], sys.argv[2])
print(response)