terraform {
  backend "s3" {
    region                          = "us-east-1"  # No vars allowed
    bucket                          = "nf-nvirginia"
    key                             = "graham/tfstate/dev/terraform.tfstate"
    profile                         = "management"
    shared_credentials_file         = "$HOME/.aws/credentials"
  }
}