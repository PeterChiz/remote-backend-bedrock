# main.tf
terraform {
  cloud {
    organization = "Basic_Infrastructure"
    workspaces {
      name = "remote-backend-bedrock"
    }
  }

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

# Gắn IAM Policy với IAM Role
resource "aws_iam_role_policy_attachment" "bedrock_policy_attachment" {
  role       = aws_iam_role.bedrock_access_role.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}

resource "aws_instance" "vm-user1" {
  ami = "ami-0e532fbed6ef00604"
  instance_type = "t3.micro"
  tags = {
    Name ="vm-user1"
  }
}