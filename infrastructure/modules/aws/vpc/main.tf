resource "aws_vpc" "main" {
  count = var.vpc_type == "new" ? 1 : 0

  cidr_block       = "10.7.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "main"
  }
}

module "vpc" {
  # https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest?tab=dependencies
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  count = var.vpc_type == "new" ? 1 : 0

  name = "graham-test-vpc"
  cidr = "10.9.0.0/16"
  azs  = ["us-east-1a", "us-east-1b", "us-east-1c"]

  private_subnets = [ "10.9.1.0/24", "10.9.2.0/24" ]
  public_subnets  = [ "10.9.3.0/24", "10.9.4.0/24" ]

  
  # I DO NOT LIKE THIS APPROACH BUT CANT FIND A BETTER WAY
  # Default all these to the underlying defaults in the module.
  enable_nat_gateway = lookup(var.vpc_module_options, "enable_nat_gateway", false)
  single_nat_gateway = lookup(var.vpc_module_options, "single_nat_gateway", false)
  map_public_ip_on_launch = lookup(var.vpc_module_options, "map_public_ip_on_launch", false)
  one_nat_gateway_per_az= lookup(var.vpc_module_options, "one_nat_gateway_per_az", false)

}


# Needed to add this to get existing CIDR range to limit ALB listeners
data "aws_vpc" "preexisting" {
  count = var.vpc_type == "preexisting" ? 1 : 0
  id = var.vpc_preexisting_id
}