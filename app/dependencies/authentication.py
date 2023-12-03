from fastapi import HTTPException, Depends, Header, status

def authenticate_third_party_api(api_key: str = Header(..., convert_underscores=False)):
    """
    Custom authentication decorator to check if the provided API key is valid.
    """
    valid_api_key = "your_secret_api_key"  # Replace with your actual API key
    if api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return True
