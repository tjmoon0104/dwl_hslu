# Folder where Lambda Function is located
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "lambda/"
  output_path = var.lambda_archive
}

# Historical Country Prices Lambda Function
resource "aws_lambda_function" "historical_country_prices" {
  filename         = var.lambda_archive
  function_name    = "historical_country_prices"
  role             = var.aws_role
  handler          = "historical_country_prices.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.mylayer.arn]
  timeout          = 180
}

# Current Country Prices Lambda Function
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

# Lambda Layer
resource "aws_lambda_layer_version" "mylayer" {
  layer_name          = "customlayer"
  filename            = "layer/mylayer.zip"
  compatible_runtimes = ["python3.8"]
  depends_on          = [null_resource.build_package]
}
