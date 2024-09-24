# import pandas as pd
# df = pd.read_html("https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest")

import json
import subprocess
import time
from pathlib import Path

import requests
from logger import logger

TF_GH_ROOT = "https://raw.githubusercontent.com/terraform-aws-modules"
TF_LOCAL_AWS_ROOT = "/tmp/tf/aws"

AWS_VPC_V5_1_2_ROOT = f"{TF_LOCAL_AWS_ROOT}/vpc/v5.1.2"
AWS_ELASTICACHE_1_2_3_ROOT = f"{TF_LOCAL_AWS_ROOT}/elasticache/1.2.3"
AWS_RDS_V6_9_0_ROOT = f"{TF_LOCAL_AWS_ROOT}/rds/v6.9.0"
AWS_SG_V5_2_0_ROOT = f"{TF_LOCAL_AWS_ROOT}/sg/v5.2.0"
AWS_ALB_V9_11_0_ROOT = f"{TF_LOCAL_AWS_ROOT}/alb/v9.11.0"
AWS_EKS_V20_24_2_ROOT = f"{TF_LOCAL_AWS_ROOT}/eks/v20.24.2"

targets = {
    "vpc": {
        "source_url": f"{TF_GH_ROOT}/terraform-aws-vpc/refs/tags/v5.1.2/variables.tf",
        "input_hcl": f"{AWS_VPC_V5_1_2_ROOT}/vpc.hcl",
        "input_json": f"{AWS_VPC_V5_1_2_ROOT}/vpc.json",
        "output_module_config": f"{AWS_VPC_V5_1_2_ROOT}/vpc_module_config.txt",
        "output_tfvars_config": f"{AWS_VPC_V5_1_2_ROOT}/vpc_tfvars_config.txt",
    },
    "elasticache": {
        "source_url": f"{TF_GH_ROOT}/terraform-aws-elasticache/refs/tags/v1.2.3/variables.tf",
        "input_hcl": f"{AWS_ELASTICACHE_1_2_3_ROOT}/elasticache.hcl",
        "input_json": f"{AWS_ELASTICACHE_1_2_3_ROOT}/elasticache.json",
        "output_module_config": f"{AWS_ELASTICACHE_1_2_3_ROOT}/elasticache_module_config.txt",
        "output_tfvars_config": f"{AWS_ELASTICACHE_1_2_3_ROOT}/elasticache_tfvars_config.txt",
    },
    "rds": {
        "source_url": f"{TF_GH_ROOT}/terraform-aws-rds/refs/tags/v6.9.0/variables.tf",
        "input_hcl": f"{AWS_RDS_V6_9_0_ROOT}/rds.hcl",
        "input_json": f"{AWS_RDS_V6_9_0_ROOT}/rds.json",
        "output_module_config": f"{AWS_RDS_V6_9_0_ROOT}/rds_module_config.txt",
        "output_tfvars_config": f"{AWS_RDS_V6_9_0_ROOT}/rds_tfvars_config.txt",
    },
    "security_group": {
        "source_url": f"{TF_GH_ROOT}/terraform-aws-security-group/refs/tags/v5.2.0/variables.tf",
        "input_hcl": f"{AWS_SG_V5_2_0_ROOT}/sg.hcl",
        "input_json": f"{AWS_SG_V5_2_0_ROOT}/sg.json",
        "output_module_config": f"{AWS_SG_V5_2_0_ROOT}/sg_module_config.txt",
        "output_tfvars_config": f"{AWS_SG_V5_2_0_ROOT}/sg_tfvars_config.txt",
    },
    "alb": {
        "source_url": f"{TF_GH_ROOT}/terraform-aws-alb/refs/tags/v9.11.0/variables.tf",
        "input_hcl": f"{AWS_ALB_V9_11_0_ROOT}/alb.hcl",
        "input_json": f"{AWS_ALB_V9_11_0_ROOT}/alb.json",
        "output_module_config": f"{AWS_ALB_V9_11_0_ROOT}/alb_module_config.txt",
        "output_tfvars_config": f"{AWS_ALB_V9_11_0_ROOT}/alb_tfvars_config.txt",
    },
    "eks": {
        "source_url": f"{TF_GH_ROOT}/terraform-aws-eks/refs/tags/v20.24.2/variables.tf",
        "input_hcl": f"{AWS_EKS_V20_24_2_ROOT}/eks.hcl",
        "input_json": f"{AWS_EKS_V20_24_2_ROOT}/eks.json",
        "output_module_config": f"{AWS_EKS_V20_24_2_ROOT}/eks_module_config.txt",
        "output_tfvars_config": f"{AWS_EKS_V20_24_2_ROOT}/eks_tfvars_config.txt",
    },
}

# terraform-aws-eks-pod-identity ?

key_errors = []
generate_original_input = True

for target in targets.keys():

    logger.debug(f"Processing target:'{target}'")

    # Unpack target variables
    source_url, input_hcl, input_json, output_module_config, output_tfvars_config = (
        targets[target].values()
    )

    # Create folders if not exist
    Path(input_hcl).resolve().parent.mkdir(parents=True, exist_ok=True)

    if generate_original_input == True:
        # Retrieve HCL and write to file
        r = requests.get(source_url)
        with open(input_hcl, "w") as f:
            f.write(r.text)

        # Convert HCL to JSON and write to disk
        # command = "docker run --rm -v /tmp/tfaws/vpc.hcl:/tmp/tfaws/vpc.hcl tmccombs/hcl2json /tmp/tfaws/vpc.hcl"
        command = (
            f"docker run --rm -v {input_hcl}:{input_hcl} tmccombs/hcl2json {input_hcl}"
        )
        command = command.split(" ")
        logger.debug(f"Running hcl2json container.")
        result = subprocess.run(command, capture_output=True)
        # print(result.stdout)

        # Cant figure out how to cleanly get this to wait on the completion of the subprocess. Just using crude sleep instead.
        # https://stackoverflow.com/questions/28284715/python-subprocess-popen-wait-for-completion  <-- some better options
        time.sleep(5)
        logger.debug(f"Sleep complete.")

        # Write JSON version to disk
        with open(input_json, "wb") as f:
            f.write(result.stdout)

    # Load JSON into Python object
    with open(input_json, "r") as f:
        data = json.load(f)
        data = data["variable"]

    # Purge unnecessary keys
    keys_to_purge = ["putin_khuylo"]

    for key in keys_to_purge:
        try:
            data.pop(key)
        except KeyError as e:
            continue

    # Build module lookup string and associated tfvar keys.
    module_config = []
    tfvars_config = []
    tfvars_config_var = "var.vpc_module_options"

    for key in data.keys():
        logger.debug(f"Key: {key}; Payload: {data[key]}")

        # RDS 'identifier' has no default; must compensate.
        # https://raw.githubusercontent.com/terraform-aws-modules/terraform-aws-rds/refs/tags/v6.9.0/variables.tf
        try:
            default = data[key][0]["default"]
        except KeyError as e:
            msg = f"{target} -- {key} -- {e}"
            key_errors.append(msg)
            logger.warning(msg)
            # Assume all missing defaults are strings until we see otherwise
            default = ""

        default = str(default)

        # Only works in Python3.10
        # match (default):
        #     case "True":
        #         default = "true"
        #     case "False":
        #         default = "false"
        #     case _:
        #         continue

        if default == "True":
            default = "true"
        elif default == "False":
            default = "false"
        elif default.startswith("${"):
            default = default[2:-1]
        elif (default == "") or (default == ""):
            default = '""'
        elif default == "None":
            default = "null"
        else:
            pass

        # Output of HCL2JSON starts every type with `${` and ends with `}`
        type = data[key][0]["type"]
        type = type[2:-1]

        module_string = f"{key} = lookup({tfvars_config_var}, {key}, {default})"
        tfvars_string = f"{key} = {default}"

        module_config.append(module_string)
        tfvars_config.append(tfvars_string)

        with open(output_module_config, "w") as f:
            f.write("\n".join(module_config))

        with open(output_tfvars_config, "w") as f:
            f.write("\n".join(tfvars_config))

# Console printing

# print("#" * 30)
# import pprint

# # pprint.pprint(tfvars_config)
# for entry in tfvars_config:
#     print(entry)
# print("#" * 30)
# for entry in module_config:
#     print(entry)
# # pprint.pprint(module_config)
# print("#" * 30)
