# Tạo IAM Role cho dịch vụ ec2
resource "aws_iam_role" "bedrock_access_role" {
  name = "bedrock_access_role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com" 
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

# Tạo IAM Policy để cấp quyền truy cập các API của Amazon Bedrock
resource "aws_iam_policy" "bedrock_policy" {
  name        = "bedrock_access_policy"
  description = "Policy to allow invoking models and managing provisioned throughput in Amazon Bedrock"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListModels",
          "bedrock:GetModel",
          "bedrock:CreateProvisionedModelThroughput",
          "bedrock:DescribeProvisionedModelThroughput",
          "bedrock:UpdateProvisionedModelThroughput",
          "bedrock:DeleteProvisionedModelThroughput"
        ],
        "Resource": "*"  // Nếu có ARN cụ thể của các mô hình -> thay thế "*" bằng ARN phù hợp
      }
    ]
  })
}