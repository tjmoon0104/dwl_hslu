# Select Cloud Provider as AWS
provider "aws" {
  region = var.aws_region
}

# Building
resource "null_resource" "build_package" {
  provisioner "local-exec" {
    command = "./build.sh"
  }
  triggers = {
    run_on_change = filemd5("requirements.txt")
  }
}

resource "aws_s3_bucket" "hslu-my-s3-bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_acl" "s3_acl" {
  bucket = aws_s3_bucket.hslu-my-s3-bucket.id
  acl    = "private"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "lambda/"
  output_path = var.lambda_archive
}

resource "aws_lambda_function" "test_lambda" {
  filename         = var.lambda_archive
  function_name    = "historical_country_prices"
  role             = var.aws_role
  handler          = "historical_country_prices.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.mylayer.arn]
  timeout          = 180
}

resource "aws_lambda_function" "country_prices" {
  filename         = var.lambda_archive
  function_name    = "country_prices"
  role             = var.aws_role
  handler          = "country_prices.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.mylayer.arn]
  timeout          = 180
}

resource "aws_lambda_function" "twitter_count" {
  filename         = var.lambda_archive
  function_name    = "twitter_count"
  role             = var.aws_role
  handler          = "twitter.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.mylayer.arn]
  timeout          = 180
}

resource "aws_lambda_layer_version" "mylayer" {
  layer_name          = "customlayer"
  filename            = "layer/mylayer.zip"
  compatible_runtimes = ["python3.8"]
  depends_on          = [null_resource.build_package]
}


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