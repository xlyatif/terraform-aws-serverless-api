Terraform AWS Serverless API

This project demonstrates how to build and deploy a production-style serverless REST API on AWS using Terraform as Infrastructure as Code.
The architecture uses:
* API Gateway (HTTP API v2)
* AWS Lambda (Python 3.12)
* Amazon DynamoDB (on-demand billing)
* IAM roles and scoped policies
* CloudWatch logging
All infrastructure is fully reproducible using Terraform.

Architecture Overview

The deployed serverless architecture follows this pattern:
Client → API Gateway → Lambda → DynamoDB
No EC2 instances or persistent servers are used. The solution is fully managed, event-driven, and cost-efficient.

API Design

Two REST endpoints are implemented:
POST /message Creates a new record in DynamoDB containing:
* UUID (primary key)
* Name
* Message
* Unix timestamp
GET /message/{id} Retrieves a stored message by its unique ID.
API Gateway uses AWS_PROXY integration, allowing Lambda to receive the complete HTTP request context.

Infrastructure Implementation

Terraform provisions and configures:
* DynamoDB table (PAY_PER_REQUEST billing)
* Lambda function deployment and packaging
* IAM role creation and policy attachment
* API Gateway HTTP API configuration
* Route definitions
* Lambda invocation permissions
* Tagged resources for traceability
* Output of the deployed API endpoint
Lambda packaging is automated using the Terraform archive provider, ensuring repeatable and version-controlled deployments.
All resources can be recreated or destroyed using:
terraform apply terraform destroy
This validates full infrastructure reproducibility.

Debugging & Engineering Resolution

During functional testing, the GET endpoint initially returned a 500 Internal Server Error.
CloudWatch logs identified the root cause:
TypeError: Object of type Decimal is not JSON serializable
DynamoDB returns numeric values as Decimal types, which cannot be directly serialized by Python’s json.dumps().
The issue was resolved by implementing a custom JSON serializer to convert Decimal values into integer or float types before returning API responses.
This demonstrates:
* Effective CloudWatch log analysis
* Understanding DynamoDB data types
* Resolving serialization edge cases in serverless applications
* Iterative redeployment using Terraform

Development Workflow

The full lifecycle included:
1. Provisioning infrastructure with terraform apply
2. Testing endpoints using curl
3. Debugging runtime issues via CloudWatch logs
4. Updating Lambda code
5. Redeploying using Terraform
6. Validating API functionality
7. Destroying resources to prevent unnecessary cost
This confirms the environment is fully reproducible and production-like.

Key Skills Demonstrated

* Infrastructure as Code (Terraform)
* AWS Serverless Architecture
* IAM Role and Policy Design
* API Gateway v2 Configuration
* Lambda Deployment Automation
* DynamoDB Integration
* CloudWatch Debugging
* JSON Serialization Handling
* Infrastructure Lifecycle Management

Author
Sunay I. Lyatif //  GitHub: https://github.com/xlyatif
