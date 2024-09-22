# Source: https://medium.com/@hello_9187/managing-terraform-modules-in-a-monorepo-e7e89d124d4a
# module_deployment/main.py
import os
import shutil

import boto3
import yaml

BUCKET_NAME = os.getenv("TARGET_S3_BUCKET")


if __name__ == "__main__":
    # Read in config around versions of the modules to deploy
    with open(
        f"{os.getcwd()}/infrastructure/modules/config/versions.yml", "r"
    ) as config_file:
        config = yaml.safe_load(config_file)

    # Create the S3 client
    boto_session = boto3.Session()
    s3_client = boto_session.client("s3")

    # For each module:
    # 1) Zip the configuration folder
    # 2) Upload the zipped module folder to S3 bucket
    for module, version in config.items():
        print(f"Beginning to zip module {module}-{version}.")

        zip_output_name = (
            f"{os.getcwd()}/infrastructure/modules/{module}/{module}-{version}"
        )
        directory_name = f"{os.getcwd()}/infrastructure/modules/{module}/"

        shutil.make_archive(zip_output_name, "zip", directory_name)
        print(f"Done zipping module {module}-{version}.")

        print(f"Uploading {module}-{version} to S3.")
        s3_client.upload_file(
            f"{zip_output_name}.zip", BUCKET_NAME, f"{module}/{version}.zip"
        )
        print(f"Done uploading {module}-{version} to S3.")
