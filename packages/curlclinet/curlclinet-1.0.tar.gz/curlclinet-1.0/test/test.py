import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from SimpleClient import SimpleClient

headers = {
    'authority': 'www.instagram.com',
    'accept': '*/*',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'csrftoken=4wlwa0hBYMQLUCYPCcpq0J; dpr=3.0234789848327637; mid=ZuQrKAAEAAET4NS-py8kAzKJjYXk; datr=KCvkZvAOjW6gq1A11Zsdt94h; ig_did=DBB463FD-A63D-4893-9DFC-12B5D65BBF17; wd=891x925',
    'origin': 'https://www.instagram.com',
    'referer': 'https://www.instagram.com/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '""',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-asbd-id': '129477',
    'x-csrftoken': '4wlwa0hBYMQLUCYPCcpq0J',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': '0',
    'x-instagram-ajax': '1016468584',
    'x-requested-with': 'XMLHttpRequest',
    'x-web-device-id': 'DBB463FD-A63D-4893-9DFC-12B5D65BBF17',
}

data = {
    'enc_password': '#PWD_INSTAGRAM_BROWSER:10:1726229303:Ad9QAA5jje6BXMIirglmCuBz0a21gCGgjFm7paqgIsXe7TwlJmaIyzvDV3v9szvEb7+GsrzFjRj4jMtar4XXQNt/CbC6Vjm5sGxHfb4YfxgxGVPdlvUu06XXyWjrXY2/j6JxpSTbOPn6B19S5Ts=',
    'caaF2DebugGroup': '0',
    'loginAttemptSubmissionCount': '0',
    'optIntoOneTap': 'false',
    'queryParams': '{}',
    'trustedDeviceRecords': '{}',
    'username': 'mahos9966',
}


client = SimpleClient('GET', 'https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data)

print("Full", client.text)
print("Nuon", client.cookies)
print("po", client.json())
print(client.headers)
client = SimpleClient('POST', 'https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data)
print("Full", client.text)
print("Nuon", client.cookies)
print("po", client.json())
print(client.headers)