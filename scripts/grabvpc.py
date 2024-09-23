# import pandas as pd
# df = pd.read_html("https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest")

import subprocess

import requests

TF_ROOT = (
    "https://raw.githubusercontent.com/terraform-aws-modules/terraform-aws-vpc/refs"
)

targets = {
    "vpc": {
        "source_url": f"{TF_ROOT}/heads/master/variables.tf",
        "output_hcl": "/tmp/tfaws/vpc.hcl",
        "output_json": "/tmp/tfaws/vpc.json",
    }
}

url = f"{TF_ROOT}/heads/master/variables.tf"
file = "/tmp/tfaws/vpc.hcl"
# Add test to create folder if not exists
r = requests.get(url)
with open(file, "w") as f:
    f.write(r.text)

# command = "docker run --rm hello-world"
# command = command.split(" ")
# result = subprocess.run(command, capture_output=True)

command = "docker run --rm -v /tmp/tfaws/vpc.hcl:/tmp/tfaws/vpc.hcl tmccombs/hcl2json /tmp/tfaws/vpc.hcl"
command = command.split(" ")
result = subprocess.run(command, capture_output=True)
print(result.stdout)

file = "/tmp/tfaws/vpc.json"
with open(file, "wb") as f:
    f.write(result.stdout)

"""
{
    "variable": {
        "amazon_side_asn": [
            {
                "default": "64512",
                "description": "The Autonomous System Number (ASN) for the Amazon side of the gateway. By default the virtual private gateway is created with the current default Amazon ASN",
                "type": "${string}"
            }
        ],
        "azs": [
            {
                "default": [],
                "description": "A list of availability zones names or ids in the region",
                "type": "${list(string)}"
            }
        ],
        "cidr": [
            {
                "default": "10.0.0.0/16",
                "description": "(Optional) The IPv4 CIDR block for the VPC. CIDR can be explicitly set or it can be derived from IPAM using `ipv4_netmask_length` \u0026 `ipv4_ipam_pool_id`",
                "type": "${string}"
            }
        ],
"""


exit()


purge_words = ["  description", "  type", "###", "# ", "putin_khuylo"]


print("=============== TFVARS =====================")
print("\n".join(entries))

print("=============== MODULE =====================")
for entry in entries:
    key, value = entry.split("=", maxsplit=1)
    print(f'{key} = lookup(var.vpc_module_options, "{key}", {value})')


"""
variable "create_flow_log_cloudwatch_iam_role" {
  description = "Whether to create IAM role for VPC Flow Logs"
  type        = bool
  default     = false
}

variable "flow_log_cloudwatch_iam_role_arn" {
  description = "The ARN for the IAM role that's used to post flow logs to a CloudWatch Logs log group. When flow_log_destination_arn is set to ARN of Cloudwatch Logs, this argument needs to be provided"
  type        = string
  default     = ""
}

--- TO ---
manage_default_network_acl
  default     = true
}
default_network_acl_name
  default     = null
}
default_network_acl_ingress
  default = [
    {
      rule_no    = 100
      action     = "allow"
      from_port  = 0
      to_port    = 0
      protocol   = "-1"
      cidr_block = "0.0.0.0/0"
    },
    {
      rule_no         = 101
      action          = "allow"
      from_port       = 0
      to_port         = 0
      protocol        = "-1"
      ipv6_cidr_block = "::/0"
    },
  ]
}


--- TO ---
default_network_acl_ingress =  [ tomap({ "rule_no" =  100, "action" =  "allow", "from_port" =  0, "to_port" =  0, "protocol" =  "-1", "cidr_block" =  "0.0.0.0/0", }), tomap({ "rule_no" =  101, "action" =  "allow", "from_port" =  0, "to_port" =  0, "protocol" =  "-1", "ipv6_cidr_block" =  "::/0", }), ]
default_network_acl_egress =  [ tomap({ "rule_no" =  100, "action" =  "allow", "from_port" =  0, "to_port" =  0, "protocol" =  "-1", "cidr_block" =  "0.0.0.0/0", }), tomap({ "rule_no" =  101, "action" =  "allow", "from_port" =  0, "to_port" =  0, "protocol" =  "-1", "ipv6_cidr_block" =  "::/0", }), ]
default_network_acl_tags =  {}
manage_default_route_table =  true
"""
