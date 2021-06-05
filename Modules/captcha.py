# Auto Almost Everything
# Youtube Channel https://www.youtube.com/c/AutoAlmostEverything
# Please read README.md carefully before use

# Solve captcha by using https://2captcha.com?from=11528745.

import requests, time


class Captcha:
    def __init__(self, service, APIKey):
        self.service = service
        self.APIKey = APIKey

    def getAPIKey(self):
        return self.APIKey

    def reCaptcha(self, sitekey, pageurl):
        if self.service == '2Captcha':
            link = 'http://2captcha.com/in.php?key=%s&method=userrecaptcha&googlekey=%s&pageurl=%s'
            req = requests.get(link % (self.APIKey, sitekey, pageurl), timeout=30)
            id = ''
            if 'OK|' in req.text:
                id = req.text.split('|')[1]
            result = ''
            if id != '':
                while True:
                    time.sleep(2.5)
                    link = 'http://2captcha.com/res.php?key=%s&action=get&id=%s'
                    req = requests.get(link % (self.APIKey, id), timeout=30)
                    if 'OK|' in req.text:
                        result = req.text.split('|')[1]
                        break
            return result
        elif self.service == 'CapMonster':
            link = 'https://api.capmonster.cloud/createTask'
            json = {
                'clientKey': self.APIKey,
                'task':
                    {
                        'type': 'NoCaptchaTaskProxyless',
                        'websiteURL': pageurl,
                        'websiteKey': sitekey,
                    }
            }
            req = requests.post(link, json=json, timeout=30)
            id = ''
            if 'errorId' in req.json() and req.json()['errorId'] == 0 and 'taskId' in req.json():
                id = req.json()['taskId']
            result = ''
            if id != '':
                while True:
                    time.sleep(2.5)
                    link = 'https://api.capmonster.cloud/getTaskResult'
                    json = {
                        'clientKey': self.APIKey,
                        'taskId': id,
                    }
                    req = requests.post(link, json=json, timeout=30)
                    if 'errorId' in req.json() and req.json()['errorId'] == 0 and 'status' in req.json() and req.json()[
                        'status'] == 'ready' and 'solution' in req.json() and 'gRecaptchaResponse' in req.json()[
                        'solution']:
                        result = req.json()['solution']['gRecaptchaResponse']
                        break
            return result
        elif self.service == 'AntiCaptcha':
            link = 'https://api.anti-captcha.com/createTask'
            json = {
                'clientKey': self.APIKey,
                'task':
                    {
                        'type': 'RecaptchaV2TaskProxyless',
                        'websiteURL': pageurl,
                        'websiteKey': sitekey,
                    }
            }
            req = requests.post(link, json=json, timeout=30)
            id = ''
            if 'errorId' in req.json() and req.json()['errorId'] == 0 and 'taskId' in req.json():
                id = req.json()['taskId']
            result = ''
            if id != '':
                while True:
                    time.sleep(2.5)
                    link = 'https://api.anti-captcha.com/getTaskResult '
                    json = {
                        'clientKey': self.APIKey,
                        'taskId': id,
                    }
                    req = requests.post(link, json=json, timeout=30)
                    if 'errorId' in req.json() and req.json()['errorId'] == 0 and 'status' in req.json() and req.json()[
                        'status'] == 'ready' and 'solution' in req.json() and 'gRecaptchaResponse' in req.json()[
                        'solution']:
                        result = req.json()['solution']['gRecaptchaResponse']
                        break
            return result
