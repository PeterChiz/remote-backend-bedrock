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