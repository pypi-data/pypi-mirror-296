def get_secret_value(secret_name,key_vault_name) -> str:
    import notebookutils
    kv = f'https://{key_vault_name}.vault.azure.net/' #insert the right key valut URI
    secret = notebookutils.credentials.getSecret(kv,secret_name)
    return(secret)