module "testvpc" {
    # source = "s3::https://s3.amazonaws.com/nf-nvirginia/aws/vpc/1.0.0.zip"
    source = "../../modules/aws/vpc/"

    vpc_type = var.vpc_type
    vpc_preexisting_id = var.vpc_preexisting_id
}