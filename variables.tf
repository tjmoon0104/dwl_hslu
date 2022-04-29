variable "aws_region" {
  description = "The AWS region to create things"
  default     = "us-east-1"
}

variable "aws_role" {
  type    = string
  default = "arn:aws:iam::532621252424:role/robomaker_students"
}

variable "lambda_archive" {
  type    = string
  default = "deploy/lambda_function.zip"
}

variable "dependencies_archive" {
  type    = string
  default = "layer/mylayer.zip"
}

