variable "jenkins_pub_key" {
  type = string
}

variable "executor_access_pub_keys" {
  type = list(string)
}

variable "global_access_key_name" {
  type    = string
  default = "tvm_ci_creds"
}

variable "autoscaler_name" {
  type = string
}

variable "agent_instance_type" {
  default     = "c4.2xlarge"
  type = string
  description = "The instance type runners will be created on."
}

variable "image_family" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_groups" {
  type = list(string)
}

variable "min_size" {
  type    = number
  default = 0
}

variable "max_size" {
  type = number
}

variable "jenkins_instance_profile" {
  type = string
}

variable "on_demand_base_capacity" {
  type = number
}

variable "on_demand_percentage_above_base_capacity" {
  type = number
}
