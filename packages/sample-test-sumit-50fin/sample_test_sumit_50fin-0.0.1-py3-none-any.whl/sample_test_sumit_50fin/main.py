from urllib.parse import urlencode
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from clients import (NSDL_EMAIL, NSDL_PAN, NSDL_PHONE, NSDL_PLEDGOR_CLIENT_ID, 
                     NSDL_PLEDGOR_DP_ID, NSDL_REQUESTOR_ID, NSDL_REQUESTOR_NAME,
                     NSDL_PLEDGEE_CLIENT_ID, NSDL_PLEDGEE_DP_ID)
from collections import OrderedDict
import json
from nsdl import encrypt_aes_cbc_256_data, nsdl_signature, get_nsdl_headers
app = FastAPI()

from datetime import datetime
# app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

# async def abc():
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

def encrypt(message, key):
    backend = default_backend()
    iv = b'\x00' * 16  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return b64encode(ciphertext).decode('utf-8')

def decrypt(ciphertext, key):
    backend = default_backend()
    iv = b'\x00' * 16  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    ciphertext = b64decode(ciphertext.encode('utf-8'))
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_data) + unpadder.finalize()
    return message.decode('utf-8')

# Example usage
# key = b'IN00003812345678'  # 256-bit key
# message = '{"ordrDtls": {"secType": "00", "pledgeDetail": {"pledgorDpId": "IN302871", "pledgorClientId": "44150207", "pledgorPanNo": "SANDP3456Y", "executionDate": "2024-05-21", "pledgeAgreementNo": "1234567890", "pledgeClosureDate": "2025-04-09", "pledgeeDpId": "IN303358", "pledgeeClientId": "10221147", "pledgorMobile": "9137650686", "pledgorEmailId": "darpan@50fin.in", "pledgorDob": "1981-05-26", "pledgorClientName": "50Fin", "eligibleLoanAmt": "50000000", "minimumPledgeAmount": "25000", "filler1": "", "filler2": "", "filler3": ""}}}'
# encrypted_message = encrypt(message.encode('utf-8'), key)
# # encrypted_message = "pJYUmmWeecrFeopjVzsoRi+j3tpg9K8vN2rVX7L3ObRwFFhv3Evs1ojUXDDgNP2GacRek83reKxemTrGajU5+VdP0dPeJ7OHIenOpbLEEnE2Hd7BGOWg1MyYN1IW0ff1PocGSdcKXtaqTCEI1ZV9e4GEe/gL11Hti2CyEJE+Nk8SoVPCIKSxzBNyithFv9fz/SctdMc+iFRJwuN/px5RKyen7VeeBn5m/seWnwM3RAnquaP3vfqkxj0536nIwCzekAchDklZKqEoZfBE0b9Py+CeZWRtWnDWdjpGBsyarQp3s6AVRyH+VdycwWi81GIHLfBFap2WQSA6bwst+sE4T3EzdOqRB+C2VyNwWIWlT4bjGnGMiuUakg3UkzePit2uvXsASSo9amVbq+GqcATYTqIyhNSdo0lW5w84kuYutgeeY1oLadQniFzX3KbiZZt094vu16apFbPlQV5N9gDhTS4vwi/XSGqdBvFCkJaqJI4t3FbEsXvc814IdUZ/v+3iN9FkaYAo84iEpF0LfE4p/tOIBvZ6y8CH1uwSyazrGJeEagzwFS0PswleBFlf2VCKiRbRFWmoy1Eqa77++u5zEeG6WMMRTPdlh0W0LKy4moHScSsFiG0fY4NDUbOIdU8slzMxBy1PJzxWvqETZP5ekCgu5WaaE8nz/odivbxNExGoB9Z5f1SucegRSzR5E3E0xhXbE6yozvh6zJvOqtLbkQ=="
# decrypted_message = decrypt(encrypted_message, key)

# print("Original message:", message)
# print("Encrypted message:", encrypted_message)
# print("Decrypted message:", decrypted_message)


async def decrypt1(ciphertext_base64, secret_key):
    import base64
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend

    # def aes_decrypt(ciphertext_base64, secret_key):
        # Decode the base64 encoded ciphertext
    secret_key = secret_key.encode()
    ciphertext = base64.b64decode(ciphertext_base64)
    
    # Ensure the secret key is 32 bytes (256 bits) for AES-256
    if len(secret_key) not in (16, 24, 32):
        raise ValueError("Invalid key size: key must be 16, 24, or 32 bytes long")
    
    # Initialization vector (IV) - assuming the first 16 bytes of the ciphertext contain the IV
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    
    # Create a Cipher object using the secret key and IV
    cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Perform the decryption
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    
    # Unpad the plaintext (PKCS#7 padding)
    pad_length = padded_plaintext[-1]
    plaintext = padded_plaintext#[:-pad_length]
    
    return plaintext.decode()

# Example usage
# ciphertext_base64 = "pJYUmmWeecrFeopjVzsoRi+j3tpg9K8vN2rVX7L3ObRwFFhv3Evs1ojUXDDgNP2GacRek83reKxemTrGajU5+VdP0dPeJ7OHIenOpbLEEnE2Hd7BGOWg1MyYN1IW0ff1PocGSdcKXtaqTCEI1ZV


@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    # key = f"{NSDL_REQUESTOR_ID}12345678"
    # encrypted_data = "pJYUmmWeecrFeopjVzsoRi+j3tpg9K8vN2rVX7L3ObRwFFhv3Evs1ojUXDDgNP2GacRek83reKxemTrGajU5+VdP0dPeJ7OHIenOpbLEEnE2Hd7BGOWg1MyYN1IW0ff1PocGSdcKXtaqTCEI1ZV9e4GEe/gL11Hti2CyEJE+Nk8SoVPCIKSxzBNyithFv9fz/SctdMc+iFRJwuN/px5RKyen7VeeBn5m/seWnwM3RAnquaP3vfqkxj0536nIwCzekAchDklZKqEoZfBE0b9Py+CeZWRtWnDWdjpGBsyarQp3s6AVRyH+VdycwWi81GIHLfBFap2WQSA6bwst+sE4T3EzdOqRB+C2VyNwWIWlT4bjGnGMiuUakg3UkzePit2uvXsASSo9amVbq+GqcATYTqIyhNSdo0lW5w84kuYutgeeY1oLadQniFzX3KbiZZt094vu16apFbPlQV5N9gDhTS4vwi/XSGqdBvFCkJaqJI4t3FbEsXvc814IdUZ/v+3iN9FkaYAo84iEpF0LfE4p/tOIBvZ6y8CH1uwSyazrGJeEagzwFS0PswleBFlf2VCKiRbRFWmoy1Eqa77++u5zEeG6WMMRTPdlh0W0LKy4moHScSsFiG0fY4NDUbOIdU8slzMxBy1PJzxWvqETZP5ekCgu5WaaE8nz/odivbxNExGoB9Z5f1SucegRSzR5E3E0xhXbE6yozvh6zJvOqtLbkQ=="
    # print(decrypt(encrypted_data, key.encode()))

    # message = '{"ordrDtls": {"secType": "00", "pledgeDetail": {"pledgorDpId": "IN302871", "pledgorClientId": "44150207", "pledgorPanNo": "SANDP3456Y", "executionDate": "2024-05-21", "pledgeAgreementNo": "1234567890", "pledgeClosureDate": "2025-04-09", "pledgeeDpId": "IN303358", "pledgeeClientId": "10221147", "pledgorMobile": "9137650686", "pledgorEmailId": "darpan@50fin.in", "pledgorDob": "1981-05-26", "pledgorClientName": "50Fin", "eligibleLoanAmt": "50000000", "minimumPledgeAmount": "25000", "filler1": "", "filler2": "", "filler3": ""}}}'
    # print(encrypt(message.encode(), key.encode()))
    # return

    nsdl_pledgor_dp_id = NSDL_PLEDGOR_DP_ID
    nsdl_pledgor_client_id = NSDL_PLEDGOR_CLIENT_ID
    nsdl_pan = NSDL_PAN
    nsdl_phone = NSDL_PHONE
    nsdl_email = NSDL_EMAIL
    key = f"{NSDL_REQUESTOR_ID}12345678"
    client_name = NSDL_REQUESTOR_NAME
    request_time = '2020-12-17T14:24:53+0530'
    nsdl_pledgee_dp_id = NSDL_PLEDGEE_DP_ID
    nsdl_pledgee_client_id = NSDL_PLEDGEE_CLIENT_ID

    ordered_dict = OrderedDict()
    ordered_dict['pledgorDpId'] = nsdl_pledgor_dp_id
    ordered_dict['pledgorClientId'] = nsdl_pledgor_client_id
    ordered_dict['pledgorPanNo'] = nsdl_pan
    ordered_dict['executionDate'] = '2024-05-22'
    ordered_dict['pledgeAgreementNo'] = '1234567890'
    ordered_dict['pledgeClosureDate'] = '2025-04-09'
    ordered_dict['pledgeeDpId'] = nsdl_pledgee_dp_id
    ordered_dict['pledgeeClientId'] = nsdl_pledgee_client_id
    # ordered_dict['pledgeeMobileNo'] = nsdl_phone
    ordered_dict['pledgorMobile'] = nsdl_phone
    ordered_dict['pledgorEmailId'] = nsdl_email
    ordered_dict['pledgorDob'] = '1981-05-26'
    ordered_dict['pledgorClientName'] = client_name
    ordered_dict['eligibleLoanAmt'] = '50000000'
    ordered_dict['minimumPledgeAmount'] = '25000'
    ordered_dict['filler1'] = ''
    ordered_dict['filler2'] = ''
    ordered_dict['filler3'] = ''

    new_ordered_dict = OrderedDict()
    # new_ordered_dict['clientid'] = NSDL_REQUESTOR_ID
    new_ordered_dict['secType'] = '00'
    new_ordered_dict['pledgeDetail'] = ordered_dict

    # payload = json.dumps(new_ordered_dict)
    payload = json.dumps({"ordrDtls": new_ordered_dict})
    print("Payload is ", payload)
    
    # payload1 = json.dumps({
    #     'ordrDtls': {
    #         'secType': '00',
    #         'pledgeDetail': {
    #             'pledgeAgreementNo': '1234567890',
    #             'pledgorDPId': nsdl_pledgor_dp_id,
    #             'pledgorClientId': nsdl_pledgor_client_id,
    #             'pledgorPanNo' : nsdl_pan,
    #             'executionDate': datetime.now().strftime("%Y-%m-%d"),
    #             'pledgeClosureDate': "2025-04-09",
    #             'pledgeeDPId': nsdl_pledgee_dp_id,
    #             'pledgeeClientId': nsdl_pledgee_client_id,
    #             'pledgorMobile': '9111111111',
    #             # 'pledgeeMobileNo': nsdl_phone,
    #             'eligibleLoanAmount': "50000",
    #             'pledgorEmailId': nsdl_email,
    #             'pledgorDob': '1981-05-26',
    #             'pledgorClientName': client_name,
    #             "filler1":"",
    #             "filler2":"",
    #             "filler3":""
    #         }
    #     }
    # })
    # print("Payload is ", payload)
    # payload = "{\"ordrDtls\":{\"secType\":\"01\",\"pledgeDetail\":{\"pledgorDpId\":\"IN302871\",\"pledgorClientId\":\"42949363\",\"pledgorPanNo\":\"SANDP3456Y\",\"executionDate\":\"2022-05-18\",\"pledgeClosureDate\":\"2025-09-02\",\"pledgeAgreementNo\":\"12345678901234567890\",\"pledgeeDpId\":\"IN302871\",\"pledgeeClientId\":\"42949398\",\"pledgorMobile\":\"9168899166\",\"eligibleLoanAmt\":\"1\",\"pledgorEmailId\":\"testuser@nsdl.com\",\"pledgorDob\":\"2000-02-13\",\"pledgorClientName\":\"Bajaj Finance\"}}}"
    # _, encrypted_data = encrypt(payload, key)
    encrypted_data = encrypt(payload.encode(), key.encode())
    # encrypted_data = await get_encrypted_payload(payload.encode('utf-8'), key)
    print(f"encrypted_data is {encrypted_data}")
    # print(f"key is {key}")
    # encrypted_data = "pJYUmmWeecrFeopjVzsoRi+j3tpg9K8vN2rVX7L3ObRwFFhv3Evs1ojUXDDgNP2GacRek83reKxemTrGajU5+VdP0dPeJ7OHIenOpbLEEnE2Hd7BGOWg1MyYN1IW0ff1PocGSdcKXtaqTCEI1ZV9e4GEe/gL11Hti2CyEJE+Nk8SoVPCIKSxzBNyithFv9fz/SctdMc+iFRJwuN/px5RKyen7VeeBn5m/seWnwM3RAnquaP3vfqkxj0536nIwCzekAchDklZKqEoZfBE0b9Py+CeZWRtWnDWdjpGBsyarQp3s6AVRyH+VdycwWi81GIHLfBFap2WQSA6bwst+sE4T3EzdOqRB+C2VyNwWIWlT4bjGnGMiuUakg3UkzePit2uvXsASSo9amVbq+GqcATYTqIyhNSdo0lW5w84kuYutgeeY1oLadQniFzX3KbiZZt094vu16apFbPlQV5N9gDhTS4vwi/XSGqdBvFCkJaqJI4t3FbEsXvc814IdUZ/v+3iN9FkaYAo84iEpF0LfE4p/tOIBvZ6y8CH1uwSyazrGJeEagzwFS0PswleBFlf2VCKiRbRFWmoy1Eqa77++u5zEeG6WMMRTPdlh0W0LKy4moHScSsFiG0fY4NDUbOIdU8slzMxBy1PJzxWvqETZP5ekCgu5WaaE8nz/odivbxNExGoB9Z5f1SucegRSzR5E3E0xhXbE6yozvh6zJvOqtLbkQ=="
    request_reference = datetime.now().strftime("%Y%m%d%H%M%S%f")
    # Additional parameters
    signature, is_valid = nsdl_signature(payload)
    if not is_valid:
        session.close()
        raise HTTPException(status_code=400, detail=ERROR_MESSAGE['nsdl-signature-invalid'])

    """
    yyyy-MM-dd'T'HH:mm:ssZ
    """

    params = {
        'transactionType': 'TPL',
        'requestor': NSDL_REQUESTOR_NAME,
        'requestorId': NSDL_REQUESTOR_ID,
        'requestReference': request_reference[:16],
        'requestTime': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), # '2020-12-17T14:24:53+0530',
        "orderReqDtls": encrypted_data,
        "digitalSignature": signature
    }
    print(params, '-----------------------')
    # Convert payload to JSON and URL-encode
    #encoded_payload = urllib.parse.quote(json.dumps(payload))

    # Build full URL
    #full_url = f"{base_url}{urllib.parse.urlencode(params)}&orderReqDtls={encrypted_data}"
    encoded_params = urlencode(params)

    # Combine the base URL and encoded parameters
    # full_url = base_url + '?' + encoded_params
    # full_url = f"{base_url}{params}&orderReqDtls={encrypted_data}"
    # signature, is_valid = nsdl_signature(full_url)
    # print(signature, is_valid)


    #request_reference = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    # headers = get_nsdl_headers(signature, request_reference)
    # print(f"going to hit url {full_url}")
    # response = requests.request("POST", url=full_url, headers=headers)
    # print(response)
    # print(response.text)

    return templates.TemplateResponse(
        request=request, name="login.html", context=params
    )


@app.get("/redirect")
async def digilocker_redirect(request: Request):
    return RedirectResponse("https://api-dev.50fin.in/digilocker_webhook")


@app.get("/digilocker", response_class=HTMLResponse)
async def digilocker(request: Request):
    return templates.TemplateResponse(
        request=request, name="digilocker.html", context={"request": request}
    )

@app.get("/locker", response_class=HTMLResponse)
async def digilocker(request: Request):
    return RedirectResponse("/demo")

@app.get("/demo", response_class=HTMLResponse)
async def digilocker(request: Request):
    return get_html_response("123456", "completed")

def get_html_response(trans_id: str, status: str):
    html_content = f"""
            <html>
            <head>

                <script type="text/javascript">
                    function performCallback() {{
                        // Perform necessary actions
                        var responseData = {{ transactionId: '{trans_id}', status: '{status}' }};
                        console.log("inside function");
                        // Trigger the callback by sending data to a custom URL
                        window.location.href = 'fiftyfinapp://callback?data=' + encodeURIComponent(JSON.stringify(responseData));
                        window.close();
                    }}

                    //performCallback();
                    //console.log("after function");
                    //setTimeout(performCallback, 1000);
                    function abc(){{
                        console.log("in the function");
                        window.close();
                        console.log("after window close");
                    }}
                    //setTimeout(abc, 1000);
                    function getOS() {{
                      const userAgent = window.navigator.userAgent,
                          platform = window.navigator?.userAgentData?.platform || window.navigator.platform,
                          macosPlatforms = ['macOS', 'Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
                          windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
                          iosPlatforms = ['iPhone', 'iPad', 'iPod'];
                      let os = null;
                      let href = null
                      var responseData = {{ transactionId: '123456', status: 'completed' }};
                      console.log("inside function");
                      // Trigger the callback by sending data to a custom URL


                      if (macosPlatforms.indexOf(platform) !== -1) {{
                        os = 'Mac OS';
                        href = 'http://localhost:3000/callback?data=' + encodeURIComponent(JSON.stringify(responseData));
                      }} else if (iosPlatforms.indexOf(platform) !== -1) {{
                        os = 'iOS';
                        href = 'fiftyfinapp://callback?data=' + encodeURIComponent(JSON.stringify(responseData));
                      }} else if (windowsPlatforms.indexOf(platform) !== -1) {{
                        os = 'Windows';
                        href = 'http://localhost:3000/callback?data=' + encodeURIComponent(JSON.stringify(responseData));
                      }} else if (/Android/.test(userAgent)) {{
                        os = 'Android';
                        //href = 'fiftyfinapp://callback?data=' + encodeURIComponent(JSON.stringify(responseData));
                        href = 'fiftyfinapp://callback';
                        //setTimeout(performCallback, 10000);
                        //window.open("", "_blank", "");
                        //window.close();
                      }} else if (/Linux/.test(platform)) {{
                        os = 'Linux';
                        href = 'http://localhost:3000/callback?data=' + encodeURIComponent(JSON.stringify(responseData));
                      }}

                      return href;
                    }}

                    window.location.href = getOS()
                    window.open("", "_blank", "");
                    window.close();
                    //performCallback();
                    //alert(getOS());

                </script>
            </head>
            <body>
                <h1>Success</h1>
                <p>You can close this window now.</p>
                <button onclick="performCallback()">Complete Transaction</button>
            </body>
            </html>
            """
    return html_content

@app.get("/bajaj_payment", response_class=HTMLResponse)
def bajaj_payment(request: Request):
    data = {
        "url": "https://uatpayments.bajajfinserv.in/Paymentgateway/Payments/Direct_Loan_Payment",
        # "url": "https://payment.bajajfinserv.in/Payments/Payment_Error.aspx",
        "data": "50fintechPL|52620240912125620|100.0|526|Sumit_Singh|LAS_PartPayment|194413|NA|NA|https://api-dev.50fin.in/piramal_digilocker_webhook|14f3b53ce4a424ff690a786da00be70fdbb974d60f457bbebe18ab6fbf606c8b"
    }
    return templates.TemplateResponse(
        request=request, name="bajaj_payment.html", context=data
    )

@app.get("/piramal_payment", response_class=HTMLResponse)
def bajaj_payment(request: Request):
    data = {
        "amount": 10000,
        "amount_due": 10000,
        "amount_paid": 0,
        "attempts": 0,
        "created_at": 1725627790,
        "currency": "INR",
        "entity": "order",
        "id": "order_OttGB8cP6IocGl",
        "notes": [],
        "offer_id": None,
        "receipt": "49:2378:20240906183310",
        "status": "created",
        "key_id": "rzp_test_bfM0dJUeEtxgMA",
        "prefill": {
        "name": "Mungara",
        "email": "harsh@50fin.in",
        "contact": "9586232146"
        }
    }
    return templates.TemplateResponse(
        request=request, name="piramal_payment.html", context=data
    )
