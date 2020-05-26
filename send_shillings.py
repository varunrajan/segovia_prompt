from base64 import b64encode
from ecdsa import SigningKey
from ecdsa.util import sigencode_der
from uuid import UUID
import hashlib
import json
import requests
import uuid
import request_function

# Define function to send requests to API
def send_request_to_gateway(url, request_params, key_id, private_key_filename):

    # Load private key.
    with open(private_key_filename, "r") as keyfile:
        signing_key = SigningKey.from_pem(keyfile.read())

    # Encode request parameters as a JSON string.
    request_body = json.dumps(request_params).encode("UTF-8")

    # Generate the binary DER encoding of the signature.
    binary_signature = signing_key.sign(
        request_body, hashfunc=hashlib.sha256, sigencode=sigencode_der
    )

    # Render the Request-Signature header's value.
    base64_signature = b64encode(binary_signature).decode("ascii")
    global header_value
    header_value = "ecdsa={0}".format(base64_signature)

    # Set the required headers.
    headers = {
        "API-Version": "1.0",
        "Content-Type": "application/json",
        "Key-ID": key_id,
        "Request-Signature": header_value,
    }

    # Send the request and read the response from the payment gateway.
    response = requests.post(url, data=request_body, headers=headers)
    result = response.json()

    # Examine result and do whatever your application needs to do.
    return result


# Generate random UUIDs for Request and Transaction IDs
# Convert them to strings to be JSON serialializable
request_id = str(uuid.uuid1())
transaction_id = str(uuid.uuid4())

# Set URL for sending payments
payment_url = 'https://payment-api.thesegovia.com/api/pay'

# Set private key variable
key_id = 'er157YrM1WL'

# Define input fields to be sent to target receipient via /api/pay
payment_payload = {
    "clientId": "homework-test",
    "requestId": request_id,
    "transactions": [
        {
         "transactionId":transaction_id,
         "provider": "autodetect",
         "currency": "KES",
         "recipientAccountId":"254999999999",
         "amount": 1200,
         "name":"Sum Baadi"
        }
    ]
}

# Set private key filename as variable
private_key_file = "private-key.pem"

# Use request function to send payment
send_request_to_gateway(payment_url, payment_payload, key_id, private_key_file)

# Set input fields to be sent to /api/transactionstatus
status_url = 'https://payment-api.thesegovia.com/api/transactionstatus'

# Define fields to check against recently sent payment via /api/transactionstatus
status_payload = {
    "clientId": "homework-test",
    "requestId": request_id,
    "transactionIds": [transaction_id]
}

# Use request function to check status
send_request_to_gateway(status_url, status_payload, key_id, private_key_file)