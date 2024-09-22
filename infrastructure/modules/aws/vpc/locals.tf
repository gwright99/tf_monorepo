locals {
    # vpc_id = var.vpc_type == "new" ? module.vpc[0].vpc_id : var.vpc_existing_id
    vpc_id = var.vpc_type == "new" ? aws_vpc.main[0].id : data.aws_vpc.preexisting[0].id
}