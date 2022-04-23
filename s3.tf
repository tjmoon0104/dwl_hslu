# Create AWS S3 Bucket
resource "aws_s3_bucket" "hslu-my-s3-bucket" {
  bucket = "hslu-dwl-numbeo-data"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all1" {
  bucket = aws_s3_bucket.hslu-my-s3-bucket.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "existing-bucket-test-hslu" {
  bucket = "existing-bucket-test-hslu"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all2" {
  bucket = aws_s3_bucket.existing-bucket-test-hslu.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "gasoline-price" {
  bucket = "gasoline-price"
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
  bucket = "tweet-count"
}

resource "aws_s3_bucket_public_access_block" "s3_block_all4" {
  bucket = aws_s3_bucket.tweet-count.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

