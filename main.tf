# Select Cloud Provider as AWS
provider "aws" {
  region = var.aws_region
}

# Building Lambda Layer from Python Packages
resource "null_resource" "build_package" {
  provisioner "local-exec" {
    command = "./build.sh"
  }
  triggers = {
    run_on_change = filemd5("requirements.txt")
  }
}

# Cloud Watch Event to Trigger Lambda Function
resource "aws_cloudwatch_event_rule" "every_one_minute" {
  name                = "every-one-minute"
  description         = "Fires every one minutes"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "check_foo_every_one_minute" {
  rule      = aws_cloudwatch_event_rule.every_one_minute.name
  target_id = "lambda"
  arn       = aws_lambda_function.twitter_count.arn
}


resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.twitter_count.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_one_minute.arn
}