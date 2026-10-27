# bring-up.sh turns these into the `export` lines the reviewer uses.
output "openai_endpoint" { value = module.foundry.openai_v1_endpoint }
output "chat_deployment" { value = module.foundry.chat_deployment }
