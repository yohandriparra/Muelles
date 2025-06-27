from fastapi import Header, HTTPException

def get_api_keys_from_header(api_key_header: str = Header(default=None, alias="X-Api-Key")):
    if api_key_header is None:
        raise HTTPException(
            status_code=401,
            detail="Es requisito proporcionar una clave API para realizar este tipo de consulta."
        )
    return True