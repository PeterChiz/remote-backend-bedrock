# terraform {
#   backend "s3" {
#     bucket         = "backend-s3-bedrock"  # Tên S3 bucket
#     key            = "state/terraform.tfstate"  # Đường dẫn lưu state trong bucket
#     region         = "us-east-1"
#     encrypt        = true   # Mã hóa state file
#     dynamodb_table = "terraform-lock"  # Bảng DynamoDB để khóa state
#   }
# }
