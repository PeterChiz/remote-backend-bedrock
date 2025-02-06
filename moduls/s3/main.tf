terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.49.0"
    }
  }
  
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "aws_s3_bucket" {
  bucket = "backend-s3-bedrock"
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
