from fastapi import HTTPException, status
import httpx


def handle_httpx_exceptions(exc: Exception):
    if isinstance(exc, httpx.RequestError):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to connect to downstream service: {exc}"
        )
    elif isinstance(exc, httpx.HTTPStatusError):
        try:
            error_detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            error_detail = exc.response.text

        raise HTTPException(
            status_code=exc.response.status_code,
            detail=error_detail
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
