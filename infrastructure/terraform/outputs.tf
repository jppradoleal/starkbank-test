output "queue_url" {
  description = "The queue address"
  value = module.sqs.queue_url
}
