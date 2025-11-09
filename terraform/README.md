# Terraform Infrastructure for FHIR ML Pipeline

This directory contains the Terraform configuration for deploying the FHIR ML Pipeline infrastructure on AWS.

## Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Terraform installed** (version >= 1.0)
3. **S3 bucket** for storing Terraform state
4. **DynamoDB table** for state locking (optional but recommended)

## Setup

### 1. Configure Backend

Copy the backend configuration template:

```bash
cp terraform/backend.tf.example terraform/backend.tf
```

Edit `terraform/backend.tf` with your S3 bucket details:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "fhir-ml-pipeline/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### 2. Configure Variables

Copy the variables template:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Edit `terraform/terraform.tfvars` with your values:

```hcl
aws_region = "us-west-2"
environment = "dev"
db_password = "your-secure-password-here"
```

### 3. Initialize Terraform

```bash
cd terraform
terraform init
```

### 4. Plan and Apply

```bash
# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

## Infrastructure Components

### Networking
- **VPC** with public and private subnets
- **NAT Gateway** for private subnet internet access
- **Security Groups** for ALB, ECS tasks, and RDS

### Compute
- **ECS Cluster** for containerized services
- **Application Load Balancer** for traffic distribution

### Database
- **RDS PostgreSQL** instance for FHIR data storage
- **Encrypted storage** with automated backups

### Storage
- **S3 Bucket** for FHIR data files
- **Versioning enabled** for data protection

## GitHub Actions Integration

The infrastructure is designed to work with GitHub Actions for CI/CD:

### Required Secrets

Add these secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region (default: us-west-2)
- `DB_PASSWORD` - Database password

### Workflows

1. **terraform.yml** - Terraform plan and apply
2. **ci.yml** - Continuous integration testing
3. **deploy.yml** - Application deployment
4. **security.yml** - Security scanning

## Environment Management

### Development Environment

```bash
export TF_VAR_environment=dev
terraform apply
```

### Production Environment

```bash
export TF_VAR_environment=prod
terraform apply
```

## Security Considerations

- All resources are tagged for cost tracking
- Database passwords are stored as sensitive variables
- S3 buckets have encryption enabled
- Security groups follow least privilege principles
- RDS has automated backups and encryption

## Monitoring

- **CloudWatch Logs** for application logging
- **ECS Container Insights** for performance monitoring
- **RDS Performance Insights** for database monitoring

## Cost Optimization

- Use `db.t3.micro` for development
- Enable auto-scaling for production workloads
- Use S3 lifecycle policies for data archival
- Monitor costs with AWS Cost Explorer

## Troubleshooting

### Common Issues

1. **State lock errors**: Check DynamoDB table permissions
2. **S3 access denied**: Verify bucket policy and IAM permissions
3. **VPC limits**: Check AWS service limits in your region

### Useful Commands

```bash
# View current state
terraform show

# List all resources
terraform state list

# Import existing resources
terraform import aws_instance.example i-1234567890abcdef0

# Destroy infrastructure
terraform destroy
```

## Contributing

When making changes to the infrastructure:

1. Test changes in development environment first
2. Update documentation for new resources
3. Ensure all resources are properly tagged
4. Review security implications of changes
