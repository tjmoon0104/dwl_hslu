resource "aws_glue_catalog_database" "numbeo_catalog" {
  name = "numbeo_catalog"
}

resource "aws_glue_crawler" "numbeo_crawler" {
  database_name = aws_glue_catalog_database.numbeo_catalog.name
  name          = "numbeo_crawler"
  role          = "arn:aws:iam::532621252424:role/LabRole"

  s3_target {
    path = "s3://${aws_s3_bucket.hslu-dwl-data-warehouse.bucket}/historical_country_prices"
  }
}