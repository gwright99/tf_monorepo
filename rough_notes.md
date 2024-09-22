# Rough Notes

Notes to self:

1. See KB Terrafrom notes for source article this structure is based on.
2. Consider whether usage of AWS Terrform modules + custom logic means I must have a "module calling a module structure" (_which I dont love_).

- nth publication will overwrite pre-existing package in S3 bucket target.

- Must add `AWS_SDK_LOAD_CONFIG=true` to shell where `terraform` is being run (with GSTS) at least. https://github.com/hashicorp/terraform/issues/27192


## Problems
1) Error: User: arn:aws:iam::***:user/DevelopmentTowerUser is not authorized to perform: sts:TagSession on resource: ***

2) Run aws-actions/configure-aws-credentials@v2
/usr/bin/docker exec  418ed0db430b69f6b9e92fd66b235daa53bad697cdad47fdd3f36ee7c2241ed0 sh -c "cat /etc/*release | grep ^ID"
(node:51) NOTE: We are formalizing our plans to enter AWS SDK for JavaScript (v2) into maintenance mode in 2023.
Please migrate your code to use AWS SDK for JavaScript (v3).
For more information, check the migration guide at https://a.co/7PzMCcy
(Use `node --trace-warnings ...` to show where the warning was created)