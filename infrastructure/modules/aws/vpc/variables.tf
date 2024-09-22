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
    default = ""

    # TO DO:
    # - Evaluate based on Cloud tag?
    # - Tighten rules to specific AWS VPC ID?

    # THIS CAN ONLY WORK IN TF v1.9+
    # validation {
    #     condition = var.vpc_type == "preexisting" && length(var.vpc_preexisting_id) > 0
    #     error_message = "Variable `vpc_prexisting_id` cannot be blank."
    # }
}

variable vpc_module_options {
    type = map(bool)
}
