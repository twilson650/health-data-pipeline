# Required GitHub Secrets

This document outlines the secrets that need to be configured in your GitHub repository for the CI/CD pipelines to work properly.

## AWS Secrets

### Required for all workflows

- **`AWS_ACCESS_KEY_ID`** - AWS access key ID
- **`AWS_SECRET_ACCESS_KEY`** - AWS secret access key  
- **`AWS_REGION`** - AWS region (default: us-west-2)

### Optional AWS secrets

- **`AWS_ACCOUNT_ID`** - AWS account ID (for ECR repository URLs)
- **`S3_BUCKET_NAME`** - S3 bucket for Terraform state (if not using backend config)

## Database Secrets

- **`DB_PASSWORD`** - Database password for RDS instance

## How to Add Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret with the exact name and value

## Environment-Specific Secrets

For different environments (dev, staging, prod), you can use GitHub Environments:

1. Go to **Settings** → **Environments**
2. Create environments for `dev`, `staging`, `prod`
3. Add environment-specific secrets
4. Configure protection rules as needed

## Security Best Practices

- Use IAM roles with minimal required permissions
- Rotate secrets regularly
- Use different credentials for different environments
- Never commit secrets to version control
- Use AWS Secrets Manager for sensitive data when possible

## Example IAM Policy

Here's a minimal IAM policy for the GitHub Actions user:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-terraform-state-bucket",
                "arn:aws:s3:::your-terraform-state-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/terraform-state-lock"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ecs:*",
                "ec2:*",
                "rds:*",
                "iam:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## Troubleshooting

### Common Issues

1. **Access Denied errors**: Check IAM permissions
2. **Invalid credentials**: Verify secret values are correct
3. **Region mismatch**: Ensure AWS_REGION matches your resources
4. **S3 bucket not found**: Create the Terraform state bucket first

### Testing Secrets

You can test your secrets by running a simple workflow:

```yaml
name: Test Secrets
on: workflow_dispatch
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Test AWS credentials
        run: |
          aws sts get-caller-identity
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: ${{ secrets.AWS_REGION }}
```
