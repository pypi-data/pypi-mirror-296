import subprocess
import json
import re
#BY AHMED ALHRRANI 
#MS4
class request:
    def __init__(self, method, url, headers=None, data=None, params=None, files=None, proxies=None):
        self.method = method.upper()
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.params = params or {}
        self.files = files or {}
        self.proxies = proxies
        self.response = self._make_request()

    def _make_request(self):
        if self.method == 'GET':
            return self._get()
        elif self.method == 'POST':
            return self._post()
        else:
            raise ValueError("Unsupported method. Use 'GET' or 'POST'.")

    def _get(self):
        cmd = ['curl', '-s', self.url]
        if self.params:
            param_str = '&'.join(f'{key}={value}' for key, value in self.params.items())
            cmd.append(f'?{param_str}')
        if self.data:
            for key, value in self.data.items():
                cmd += ['--data-urlencode', f'{key}={value}']
        if self.proxies:
            cmd += ['-x', self.proxies]
        if self.files:
            for file_key, file_path in self.files.items():
                cmd += ['-F', f'{file_key}=@{file_path}']
        if self.headers:
            for header in self.headers:
                cmd += ['-H', f'{header}: {self.headers[header]}']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def _post(self):
        cmd = ['curl', '-s', '-X', 'POST', self.url]
        if self.proxies:
            cmd += ['-x', self.proxies]
        if self.params:
            param_str = '&'.join(f'{key}={value}' for key, value in self.params.items())
            cmd.append(f'?{param_str}')
        if self.data:
            for key, value in self.data.items():
                cmd += ['--data-urlencode', f'{key}={value}']
        if self.files:
            for file_key, file_path in self.files.items():
                cmd += ['-F', f'{file_key}=@{file_path}']
        if self.headers:
            for header in self.headers:
                cmd += ['-H', f'{header}: {self.headers[header]}']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    @property
    def text(self):
        return self.response

    @property
    def cookies(self):
        cookies = re.findall(r'set-cookie:\s*([^;]+)', self.response, re.IGNORECASE)
        if cookies:
            return cookies
        else:
            return None

    def json(self):
        try:
            return json.loads(self.response)
        except json.JSONDecodeError:
            return None