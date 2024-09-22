variable "aws_account" { type = string }
variable "aws_region" { type = string }
variable "aws_profile" { type = string }

# Cloud
variable "target_cloud" {
    type = string
    # default = "aws"

    validation {
        condition = contains(["aws", "azure", "gcp"], var.target_cloud)
        error_message = "Allowed values for `target_cloud` are: 'aws', 'azure', and 'gcp'."
    }
}

# VPC Type
variable "vpc_type" {
    type = string
    # default = new

    validation {
        condition = contains(["new", "preexisting"], var.vpc_type)
        error_message = "Allowed values for `vpc_type` are: 'new' and 'preexisting'."
    }
}

variable "vpc_preexisting_id" {
    type = string
    default = ""  # I do not like these defaults. Think everything should be in one view (tfvars).
      # I'm already getting confused by the connnections / lack thereof.

    # TO DO:
    # - Evaluate based on Cloud tag?
    # - Tighten rules to specific AWS VPC ID?

    # THIS CAN ONLY WORK IN TF v1.9+
    # validation {
    #     condition = var.vpc_type == "preexisting" && length(var.vpc_preexisting_id) > 0
    #     error_message = "Variable `vpc_prexisting_id` cannot be blank."
    # }

}
