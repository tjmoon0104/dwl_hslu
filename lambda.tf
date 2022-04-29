# Folder where Lambda Function is located
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "lambda/"
  output_path = var.lambda_archive
}

# Historical Country Prices Lambda Function
resource "aws_lambda_function" "numbeo_data" {
  filename         = var.lambda_archive
  function_name    = "numbeo_api_data"
  role             = var.aws_role
  handler          = "numbeo_data.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.mylayer.arn]
  timeout          = 600
  memory_size      = 512
}

resource "aws_lambda_function" "preprocess_numbeo" {
  filename         = var.lambda_archive
  function_name    = "preprocess_numbeo"
  role             = var.aws_role
  handler          = "preprocess_numbeo.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.mylayer.arn]
  timeout          = 600
  memory_size      = 512
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
  layer_name          = "customlayer1"
  filename            = "layer/mylayer.zip"
  compatible_runtimes = ["python3.8"]
  depends_on          = [null_resource.build_package]
}
