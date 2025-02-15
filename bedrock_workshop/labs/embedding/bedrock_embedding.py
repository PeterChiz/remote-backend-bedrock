'''
    - Embeddings thể hiện ý nghĩa của một đoạn văn bản dưới dạng một chuỗi số gọi là vector. 
    Có thể sử dụng các vector này để xác định mức độ tương đồng giữa các đoạn văn bản (trong bài lab này)
    - Có thể sử dụng các vector database để lưu trữ embeddings và thực hiện các tìm kiếm tương đồng một cách nhanh chóng.
    Embedding kết hợp với vector database là một thành phần cốt lõi của phương pháp RAG
'''

import json, boto3
# necessary calculations to compare vectors
from numpy import dot
from numpy.linalg import norm

# Định nghĩa hàm để lấy embedding từ AB
def get_embedding(text):
    session = boto3.Session()
    bedrock = session.client(service_name = 'bedrock-runtime')

    response = bedrock.invoke_model(
        body = json.dumps({'inputText': text}),
        modelId = 'amazon.titan-embed-text-v2:0',
        accept = 'application/json',
        contentType= 'application/json'
    )

    response_body = json.loads(response['body'].read())
    return response_body['embedding']

# Định nghĩa class để lưu trữ embedding và so sánh kết quả
class EmbedItem:
    def __init__(self, text):
        self.text = text
        self.embedding = get_embedding(text)

class ComparisionResult:
    def __init__(self, text, similarity):
        self.text = text
        self.similarity = similarity

# Định nghĩa function để so sánh sự tương đồng giữa 2 vector
def calculate_similarity(a, b):
   return dot(a, b) / (norm(a) * norm(b))

# Xây dựng danh sách các embedding để so sánh
items = []

with open('items.txt', 'r', encoding='utf8') as file:
    text_items = file.read().splitlines()

for text in text_items:
    items.append(EmbedItem(text))

'''
    - So sánh embeddings và hiển thị danh sách để cho thấy mức độ tương đồng hoặc khác biệt giữa các đoạn văn bản
        + Giá trị tương đồng bằng 1 có nghĩa là hai văn bản hoàn toàn giống nhau
        + Giá trị tương đồng càng nhỏ, embeddings càng ít giống nhau
'''

for e1 in items:
    print(f"Các kết quả khớp gần nhất cho '{e1.text}'")
    print('---------------')
    cosine_comparisons = []

    for e2 in items:
        similarity_score = calculate_similarity(e1.embedding, e2.embedding)
        cosine_comparisons.append(ComparisionResult(e2.text, similarity_score)) # Lưu so sánh vào danh sách

    cosine_comparisons.sort(key=lambda x: x.similarity, reverse= True) # Liệt kê các kết quả khớp đầu tiên

    for c in cosine_comparisons:
        print('%.6f' % c.similarity, '\t', c.text)

    print()