# Create AWS S3 Bucket
resource "aws_s3_bucket" "hslu-my-s3-bucket" {
  bucket = "hslu-dwl-numbeo-data2"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all1" {
  bucket = aws_s3_bucket.hslu-my-s3-bucket.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "gasoline-price" {
  bucket = "gasoline-price2"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all3" {
  bucket = aws_s3_bucket.gasoline-price.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "tweet-count" {
  bucket = "tweet-count2"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all4" {
  bucket = aws_s3_bucket.tweet-count.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "hslu-dwl-data-warehouse" {
  bucket = "hslu-dwl-data-warehouse"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all5" {
  bucket = aws_s3_bucket.hslu-dwl-data-warehouse.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "hslu-dwl-athena-query" {
  bucket = "hslu-dwl-athena-query"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all6" {
  bucket = aws_s3_bucket.hslu-dwl-athena-query.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

