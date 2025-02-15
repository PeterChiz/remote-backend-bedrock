'''
    - Temperature là một inference parameter ảnh hưởng đến mức độ biến đổi của các phản hồi được tạo ra bởi 
    foudation model
    - Có thể hiểu temperature như một cách để kiểm soát creativity (tính sáng tạo) và variability (mức độ biến đổi của mô hình)
     + Khi temperature = 0, không có sự biến đổi, 
     phiên bản hiện tại của model sẽ luôn trả về cùng một response cho cùng một prompt
     + Khi temperature càng cao, phản hồi sẽ có nhiều biến thể hơn. 
     Trong các tình huống sáng tạo như viết nội dung, temperature cao có thể sẽ hữu ích 
     + Trong các quy trình kinh doanh hoặc tạo code, temperature = 0 thường là lựa chọn tốt nhất
    * Nếu model được update, response có thể thay đổi so với phiên bản trước. Do đó, ngay cả khi temperature bằng không thì
    vẫn nên giả định rằng phản hồi có thể thay đổi theo thời gian
'''

import boto3, sys, time

# Instantiating the AB client, setting the prompt and setting the temperature
def get_text_response(input_content, model, temperature):
    session = boto3.Session()
    bedrock = session.client(service_name = "bedrock-runtime")

    message = {
        "role": "user",
        "content": [
            {
                "text": input_content,
            }
        ]
    }

    response = bedrock.converse(
        modelId = model,
        messages = [message],
        inferenceConfig = {
            "maxTokens": 2000,
            "temperature": temperature,
            "topP": 0.9,
            "stopSequences": []
        }
    )

    return response['output']['message']['content'][0]['text']

for i in range(2):
    response = get_text_response(sys.argv[1], sys.argv[2], float(sys.argv[3]))
    print(response, end='\n\n')
    time.sleep(60)

# nếu bị lỗi ThrottlingException
'''
import time

retries = 0
max_retries = 3  # Giới hạn số lần thử lại

while retries < max_retries:
    try:
        response = get_text_response(sys.argv[1], sys.argv[2], float(sys.argv[3]))
        print(response, end='\n')
        break  # Thoát khỏi vòng lặp nếu thành công
    except botocore.exceptions.ThrottlingException as e:
        retries += 1
        wait_time = 2 ** retries  # Thời gian chờ tăng theo cấp số nhân (2s, 4s, 8s...)
        print(f"Lỗi throttling, thử lại sau {wait_time} giây...")
        time.sleep(wait_time)
else:
    print("Đã thử lại tối đa số lần nhưng vẫn thất bại.")
'''