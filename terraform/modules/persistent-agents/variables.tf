# variable "jenkins_user" {
#   type      = string
#   default   = "octobot2"
#   sensitive = true
# }

variable "jenkins_instance_profile" {
  type = string
}

variable "jenkins_pub_key" {
  type = string
}

variable "executor_access_pub_keys" {
  type = list(string)
}

# variable "jenkins_url" {
#   type = string
# }

variable "vm_group_name" {
  type = string
}

variable "agent_attributes" {
  type = list(object({
    labels    = string
    executors = number
    prefix    = string
  }))
  description = "Information specific to each agent"
}

variable "agent_instance_type" {
  default     = "c4.2xlarge"
  type = string
  description = "The instance type runners will be created on."
}

variable "image_family" {
  type = string
}

variable "volume_size" {
  type    = number
  default = 500
}

variable "subnet_id" {
  type = string
}

variable "security_groups" {
  type = list(string)
}

variable "replicas" {
  type = number
}

variable "template_versions" {
  type = list(string)
}
