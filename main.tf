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

resource "aws_instance" "vm_01" {
  ami = "ami-04b6019d38ea93034"
  instance_type = "t2.micro"
  tags = {
    Name = "vm_01"
  }
}

# Gắn IAM Policy với IAM Role
resource "aws_iam_role_policy_attachment" "bedrock_policy_attachment" {
  role       = aws_iam_role.bedrock_access_role.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}
