variable "region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "tf-serverless-api"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "lab"
}
