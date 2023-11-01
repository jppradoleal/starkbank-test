provider "aws" {
  region = var.region
}

locals {
  tags = {
    Name = var.name
    Repository = "https://github.com/jppradoleal/starkbank-test"
  }
}

module "sqs" {
  source  = "terraform-aws-modules/sqs/aws"
  version = "4.1.0"

  name = "celery"

  tags = local.tags
}
