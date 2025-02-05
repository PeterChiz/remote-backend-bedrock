# Định nghĩa AWS resource
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.49.0"
    }
  }
  
}
# terraform { 
#   cloud { 
    
#     organization = "dev-CSC-lab" 

#     workspaces { 
#       name = "Dev-lab" 
#     } 
#   } 
# }

provider "aws"{
    region = "us-east-1"
}

