import boto3, json
import base64 # dùng để mã hóa và giải mã dữ liệu nhị phân sang Base64
from io import BytesIO # cho phép xử lý dữ liệu nhị phân

session = boto3.Session()
bedrock = session.client(service_name = 'bedrock-runtime')

# Thêm hàm chuyển đổi hình ảnh
## Function này trích xuất dữ liệu image từ respone nhận được và chuyển đổi nó sang dạng mà Streamlit có thế sử dụng
def get_respone_image_from_payload(response): # trả về ảnh dạng byte từ phản hồi của mô hình
    payload = json.loads(response.get('body').read()) #tải nội dung phản hồi vào một đối tượng json
    image = payload.get('artifacts') # trích xuất các thành phần hình ảnh
    image_data = base64.b64decode(image[0].get('base64')) # giải mã hình ảnh

    return BytesIO(image_data) # trả về một đối tượng BytesIO để client app sử dụng

def get_image_response(prompt_content):
    response = bedrock.invoke_model(
        modelId = 'stability.stable-diffusion-xl-v1',
        body = json.dumps({
            'text_prompts':[{
                'text': prompt_content
            }],
            'cfg_scale': 9, # mức độ model cố gắng khớp với prompt
            'steps': 50, # số bước khuyết tán (diffusion steps) cần thực hiện
        })
    )

    output = get_respone_image_from_payload(response) # Chuyển đổi reponse payload thành đối tượng BytesIO để clinet app sử dụng

    return output

