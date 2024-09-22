terraform {
  required_version = ">= 1.1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.12.0"
    }
  }
}

provider "aws" {
  region     = var.aws_region
  profile    = var.aws_profile
  retry_mode = "adaptive"

#   default_tags {
#     tags = var.default_tags
#   }
}