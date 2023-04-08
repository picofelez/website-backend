import json

import requests
from django.conf import settings

api_base_address = settings.SMS_PANEL_BASE_API
panel_originator = settings.SMS_ORIGINATOR
access_key = settings.SMS_PANEL_ACCESS_KEY


def send_verification_code(code, phone_number) -> bool:
    send_sms_data = {
        "pattern_code": "ps7wyiito284rm8",
        "originator": panel_originator,
        "recipient": phone_number,
        "values": {
            "verification-code": f"{code}"
        }
    }
    send_sms_req = requests.post(
        url=f"{api_base_address}/messages/patterns/send",
        data=json.dumps(send_sms_data),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'AccessKey {access_key}'
        }
    )
    if send_sms_req.json()['status'] == 'OK':
        return True
