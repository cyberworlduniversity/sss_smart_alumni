"""Google Sheets integration for registration data.

The Google Apps Script web app receives registration data and writes it to
separate Alumni / Students sheets. Passwords are deliberately never sent.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GOOGLE_SHEETS_WEB_APP_URL = os.getenv(
    "GOOGLE_SHEETS_WEB_APP_URL",
    "https://script.google.com/macros/s/AKfycbzpYqrxP7uL1Lat-0lr05Ad-FyFrVeL1FASmhAXlykKRMnQ0I6YvTI8hGF9yWqBJPfptQ/exec",
).strip()


def send_registration_to_google_sheet(user):
    """Send non-sensitive registration data to Google Sheets.

    Returns (success, message). This function never sends password fields.
    """
    if not GOOGLE_SHEETS_WEB_APP_URL:
        return False, "Google Sheets Web App URL is not configured."

    payload = {
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "email": user.email or "",
        "department": user.department or "",
        "current_job": user.current_job or "",
        "phone_number": user.phone or "",
        "role": user.role or "",
    }

    request = Request(
        GOOGLE_SHEETS_WEB_APP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            result = json.loads(raw)

        if result.get("success"):
            return True, result.get("message", "Registration data stored in Google Sheets.")

        return False, result.get("message", "Google Sheets rejected the registration data.")

    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
        return False, f"Could not send registration data to Google Sheets: {exc}"
