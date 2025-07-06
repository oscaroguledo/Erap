from rest_framework.response import Response as DRFResponse
from rest_framework import status

def Response(data=None, success=True, message=None, code=status.HTTP_200_OK):
    """
    A generic response handler for JSON responses with status, message, and data.

    Parameters:
    - data: The actual data to return (default is None).
    - success: Boolean indicating success or failure (default is True).
    - message: A message describing the response (default is None).
    - code: The HTTP status code to return (default is 200).

    Returns:
    - DRF Response: A DRF JSON response with the provided data, status, message, and status code.
    """
    # You can implement get_message_from_code if needed, or just use a default message
    r_message = message if message else "Request processed successfully"

    return DRFResponse(
        data={
            "success": success,
            "message": r_message,
            "data": data
        },
        status=code
    )
