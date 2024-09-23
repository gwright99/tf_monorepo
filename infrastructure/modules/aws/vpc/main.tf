resource "aws_vpc" "main" {
  count = var.vpc_type == "new" ? 1 : 0

  cidr_block       = "10.7.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "main"
  }
}

locals {
  # mymap = tomap({"a"= "1"})
  # # mylist = tolist(local.mymap)
  # mystring = tostring(local.mymap)

  # j = jsonencode([ { "a"=1 } ] )
  # m = tolist(local.j)

  # # default_network_acl_ingress = tostring("[${local.m}]")
  # default_network_acl_ingress = [{"a": "1"}]

  # module_ids = [ tomap({"a"="b"}) ]

  x = { 
    rule_number = 100
  }

  y = [ for key, value in local.x: { "${key}" = "${value}" } ]

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

  # default_network_acl_ingress  = lookup(var.vpc_module_options, "default_network_acl_ingress ", [ for key, value in local.x: { "${key}" => "${value}" } ])
  # default_network_acl_ingress  = lookup(var.vpc_module_options, "default_network_acl_ingress ", tolist(tomap({ a = "1"})))
  # default_network_acl_ingress  = lookup(var.vpc_module_options, "default_network_acl_ingress ", var.default_network_acl_ingress)
  default_network_acl_ingress  = lookup(var.vpc_module_options, "default_network_acl_ingress ", [{"action": "allow","cidr_block": "10.9.0.0/16","from_port": 0,"protocol": "-1","rule_no": 100,"to_port": 0}])

  #, local.default_network_acl_ingress) #  [ { "rule_no" =  "999" } ] )

}


# Needed to add this to get existing CIDR range to limit ALB listeners
data "aws_vpc" "preexisting" {
  count = var.vpc_type == "preexisting" ? 1 : 0
  id = var.vpc_preexisting_id
}