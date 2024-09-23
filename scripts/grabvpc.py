# import pandas as pd
# df = pd.read_html("https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest")

import requests

url = "https://raw.githubusercontent.com/terraform-aws-modules/terraform-aws-vpc/refs/heads/master/variables.tf"

r = requests.get(url)
# print(r.content)

entries = r.text.split("\n")

purge_words = ["  description", "  type", "###", "# ", "putin_khuylo"]
# enumerate() returns a generator and generators can't be reversed, you need to convert it to a list first.
for index, value in (list(enumerate(entries)))[::-1]:

    if any(word in value for word in purge_words) or (value == ""):
        entries.pop(index)

print(entries)

for index, value in enumerate(entries):
    if 'variable "' in value:
        key = value.split('"')[1]
        entries[index] = key

for index, value in (list(enumerate(entries)))[::-1]:
    if "}" == value:
        entries.pop(index)

for index, value in (list(enumerate(entries)))[::-1]:
    if "  default" in value:
        reduced = value.split("=")[1]
        entries[index - 1] = f"{entries[index-1]} = {reduced}"
        entries.pop(index)

print("\n".join(entries))
# THIS OUTPUT SHOULD BE OK TO USE FOR THE TFVARS (I THINK)


# Add quotes around keys so i can use tomap()
for index, value in list(enumerate(entries)):
    if value.startswith("  ") and "=" in value:
        k, v = value.split("=")
        entries[index] = f'  "{k.strip()}": {v},'

print("\n".join(entries))

# Smash them altogether
# Cant use enumerate because tuples keep original state
# for index, value in (list(enumerate(entries)))[::-1]:
for i in range(len(entries) - 1, 0, -1):
    value = entries[i]
    if value.startswith("  "):

        changed = value.lstrip()
        entries[i - 1] = f"{entries[i-1]} {changed}"
        entries.pop(i)


# default_network_acl_ingress
#   default = [
#     {
#       rule_no    = 100
#       action     = "allow"
#       from_port  = 0
#       to_port    = 0
#       protocol   = "-1"
#       cidr_block = "0.0.0.0/0"
#     },
#     {
#       rule_no         = 101
#       action          = "allow"
#       from_port       = 0
#       to_port         = 0
#       protocol        = "-1"
#       ipv6_cidr_block = "::/0"
#     },
#   ]


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
