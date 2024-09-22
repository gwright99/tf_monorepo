resource "aws_vpc" "main" {
  count = var.vpc_type == "new" ? 1 : 0

  cidr_block       = "10.7.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "main"
  }
}

# Needed to add this to get existing CIDR range to limit ALB listeners
data "aws_vpc" "preexisting" {
  count = var.vpc_type == "preexisting" ? 1 : 0
  id = var.vpc_preexisting_id
}