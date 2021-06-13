# Auto Almost Everything
# Youtube Channel https://www.youtube.com/c/AutoAlmostEverything
# Please read README.md carefully before use

# Solve captcha by using https://2captcha.com?from=11528745.

import os, time, zipfile
from datetime import datetime
import urllib.parse as urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Proxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Modules import update, captcha, notification, log

app = 'AdBTC.top'
app_path = 'https://adbtc.top'

# Browser config
opts = Options()
opts.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'  # <-- Change to your Chromium browser path, replace '\' with '\\'.
opts.add_experimental_option('excludeSwitches', ['enable-automation'])
opts.add_experimental_option('useAutomationExtension', False)
cap = DesiredCapabilities.CHROME.copy()
cap['platform'] = 'WINDOWS'
cap['version'] = '10'
proxy = 'YourProxy'  # <-- To use proxy, replace 'YourProxy' by proxy string. There are two types: IP:Port or IP:Port:User:Pass
if proxy != '' and proxy != 'YourProxy':
    if len(proxy.split(':')) == 2:
        proxies = Proxy({
            'httpProxy': proxy,
            'ftpProxy': proxy,
            'sslProxy': proxy,
            'proxyType': 'MANUAL',
        })
        proxies.add_to_capabilities(cap)
    elif len(proxy.split(':')) == 4:
        t = proxy.split(':')
        proxy_host = t[0]
        proxy_port = t[1]
        proxy_user = t[2]
        proxy_pass = t[3]
        manifest_json = '''
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                '''
        background_js = '''
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                            singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                            },
                            bypassList: ["localhost"]
                            }
                        };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    ''' % (proxy_host, proxy_port, proxy_user, proxy_pass)
        plugin_file = 'authProxy_%s_%s.zip' % (proxy_host, proxy_port)
        with zipfile.ZipFile(plugin_file, 'w') as zf:
            zf.writestr("manifest.json", manifest_json)
            zf.writestr("background.js", background_js)
        opts.add_extension(plugin_file)
chromedriver_list = ['91', '90', '89', '88', '87']
chromedriver_index = 0
chromedriver_path = '.\\Drivers\\%s.exe' % chromedriver_list[chromedriver_index]

# Account config
adbtc_cookies = [
    {
        'name': 'cf_clearance',
        # Replace by your CloudFlare session -->
        'value': 'YourCloudFlareSession',
        # <-- Replace by your CloudFlare session
        'domain': '.adbtc.top',
        'path': '/',
    },
    {
        'name': 'foradbtc',
        # Replace by your session -->
        'value': 'YourSession',
        # <-- Replace by your session
        'domain': '.adbtc.top',
        'path': '/',
    },

]

log.screen_n_file('\n\n-+- -A- -U- -T- -O- -+- -A- -L- -M- -O- -S- -T- -+- -E- -V- -E- -R- -Y- -T- -H- -I- -N- -G- -+-',
                  False)
now = datetime.now()
log.screen_n_file('\n Script starts at ' + f'{now:%d/%m/%Y %H:%M:%S}', False)
log.file('Adbtc.top session is ' + adbtc_cookies[0]['value'], False)

# Anti-captcha config
autoCaptcha = True  # <-- Change to True if you want to use 2captcha to solve the captcha.
if autoCaptcha:
    captchaServiceName = '2Captcha'  # <--- 2Captcha, CapMonster, AntiCaptcha
    # Replace by your API Key -->
    ac = captcha.Captcha(captchaServiceName, 'YourAPIKey')
    # <-- Replace by your API Key
    log.file(captchaServiceName + ' API Key is ' + ac.getAPIKey(), False)


# Choose webdriver version
def changeDriver():
    global chromedriver_index, chromedriver_path
    if chromedriver_index + 1 <= len(chromedriver_list) - 1:
        chromedriver_index += 1
        chromedriver_path = '.\\Drivers\\%s.exe' % chromedriver_list[chromedriver_index]
        return True
    return False


# Get with exception handler
def get(browser, url):
    try:
        browser.get(url)
    except:
        pass


# Switch to window relative with path
def switchWindow_Path(browser, path):
    try:
        current_window = browser.current_window_handle
        if path not in browser.current_url:
            for handle in browser.window_handles:
                if handle != current_window:
                    browser.switch_to.window(handle)
                    if path in browser.current_url:
                        break
    except:
        pass


# Close other windows not relative with path
def closeOthers_Path(browser, path):
    try:
        for handle in browser.window_handles:
            browser.switch_to.window(handle)
            if path not in browser.current_url:
                browser.close()
    except:
        pass


# Surf for BTC, rub
def Surfer():
    func = "Surf"
    func_path = '/index/'

    while True:
        log.screen_n_file('', False)
        log.screen_n_file(func.upper())

        while True:
            try:
                browser = webdriver.Chrome(desired_capabilities=cap, options=opts,
                                           executable_path=chromedriver_path)
                log.screen_n_file(
                    '[*] Decide to choose web driver version %s to run.' % chromedriver_list[chromedriver_index])
                break
            except Exception as ex:
                if 'This version of ChromeDriver only supports' in str(ex):
                    log.screen_n_file(
                        '[*] Web driver version %s is not supported your browser. Switching to other web driver...' %
                        chromedriver_list[chromedriver_index])
                    if not changeDriver():
                        log.screen_n_file(
                            '[!] All of web drivers are not supported your browser. Please update browser or download web driver.')
                        time.sleep(999999)
                else:
                    log.screen_n_file('[!] %s has exception: %s!' % (app, ex))
                    notification.notify(app, '%s has exception: %s!' % (app, ex))

        browser.set_page_load_timeout(60)
        browser.implicitly_wait(60)
        try:
            get(browser, app_path)
            time.sleep(2)
            for cookie in adbtc_cookies:
                browser.add_cookie(cookie)
            get(browser, app_path + func_path)
            while 'Checking your browser before accessing' in browser.page_source:
                time.sleep(1)
            time.sleep(2)

            main_window = browser.current_window_handle

            # Auto surfing
            link = browser.find_element_by_xpath("//a[contains(text(), 'Autosurfing')]").get_attribute('href')
            try:
                browser.execute_script('''
                    window.open(arguments[0], '_blank');
                ''', link)
                time.sleep(2)
            except:
                browser.quit()
                continue
            log.screen_n_file('[+] Start Active window surfing session.')
            browser.switch_to.window(main_window)

            while True:
                try:
                    time.sleep(0.2)

                    # Active window surfing
                    link = browser.find_element_by_xpath(
                        "//a[contains(text(), 'Active window surfing')]").get_attribute(
                        'href')
                    get(browser, link)
                    time.sleep(10)
                    browser.switch_to.window(main_window)
                    while True:
                        try:
                            time.sleep(0.2)
                            if 'https://adbtc.top/surftab/w/' in browser.page_source:
                                browser.find_elements_by_xpath("//a[contains(@href, 'https://adbtc.top/surftab/w/')]")[
                                    0].click()
                                time.sleep(2)
                                switchWindow_Path(browser, 'https://adbtc.top/surftab/w/')
                                time.sleep(10)
                                while 'Please choose one of two similar images' not in browser.title:
                                    time.sleep(1)
                                    browser.switch_to.window(browser.current_window_handle)
                                log.screen_n_file('[+] Manually choose similar images.')
                                notification.sound()
                                notification.notify(app, 'Please choose similar images!')
                                count_time = 0
                                while len(
                                        browser.window_handles) > 2 and 'Please choose one of two similar images' in browser.title:
                                    time.sleep(1)
                                    count_time += 1
                                    if count_time >= 20:
                                        break
                                if len(browser.window_handles) > 2:
                                    browser.close()
                                browser.switch_to.window(main_window)
                                log.screen_n_file('[+] Completed Active window surfing.')
                            elif 'You have watched all the websites' in browser.page_source:
                                time.sleep(10)
                                break
                            elif 'title="reCAPTCHA"' in browser.page_source:
                                while True:
                                    try:
                                        time.sleep(0.2)
                                        if autoCaptcha:
                                            log.screen_n_file('[+] Automatically solve captcha.')
                                            recaptcha = browser.find_element_by_xpath(
                                                "//iframe[contains(@title, 'reCAPTCHA')]")
                                            sitekey = ''
                                            for query in urlparse.urlparse(recaptcha.get_attribute('src')).query.split(
                                                    '&'):
                                                if 'k=' in str(query):
                                                    sitekey = str(query).split('=')[1]
                                            token = ac.reCaptcha(sitekey, browser.current_url)
                                            log.screen_n_file(
                                                '  [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))

                                            # Run callback function
                                            browser.execute_script('''
                                                document.getElementById("g-recaptcha-response").innerHTML=arguments[0];
                                            ''', token)
                                            time.sleep(1)
                                            browser.find_element_by_xpath("//input[contains(@type, 'submit')]").click()
                                            time.sleep(10)
                                            break
                                        else:
                                            log.screen_n_file('[+] Manually solve captcha.')
                                            notification.sound()
                                            notification.notify(app, 'Please solve captcha!')
                                            time.sleep(60)
                                            break
                                    except:
                                        pass
                            elif 'widget containing checkbox for hCaptcha security challenge' in browser.page_source:
                                while True:
                                    try:
                                        time.sleep(0.2)
                                        if autoCaptcha:
                                            log.screen_n_file('  [+] Automatically solve captcha.')
                                            hcaptcha = browser.find_element_by_xpath(
                                                "//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")
                                            sitekey = ''
                                            for fragment in urlparse.urlparse(
                                                    hcaptcha.get_attribute('src')).fragment.split(
                                                '&'):
                                                if 'sitekey=' in str(fragment):
                                                    sitekey = str(fragment).split('=')[1]
                                                    break
                                            token = ac.HCaptcha(sitekey, browser.current_url)
                                            log.screen_n_file(
                                                '    [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))
                                            browser.execute_script('''
                                                document.getElementsByTagName("textarea")[0].innerHTML = arguments[0];
                                                document.getElementsByTagName("form")[0].submit();
                                            ''', token)
                                            time.sleep(10)
                                            break
                                        else:
                                            log.screen_n_file('[+] Manually solve captcha.')
                                            notification.sound()
                                            notification.notify(app, 'Please solve captcha!')
                                            time.sleep(60)
                                            break
                                    except:
                                        pass
                            else:
                                time.sleep(10)
                                break
                        except:
                            pass

                    # Surf ads ₽
                    link = browser.find_element_by_xpath("//a[contains(text(), 'Surf ads ₽')]").get_attribute(
                        'href')
                    get(browser, link)
                    time.sleep(10)
                    browser.switch_to.window(main_window)
                    while True:
                        try:
                            time.sleep(0.2)
                            if '0pen' in browser.page_source or 'Opеn' in browser.page_source:
                                while True:
                                    detect_string = '0pen'
                                    if 'Opеn' in browser.page_source:
                                        detect_string = 'Opеn'
                                    open_btns = browser.find_elements_by_xpath(
                                        "//a[contains(text(), '" + detect_string + "')]")
                                    for open_btn in open_btns:
                                        try:
                                            open_btn.click()
                                        except:
                                            pass
                                    time.sleep(0.2)
                                    if len(browser.window_handles) > 2:
                                        break
                                time.sleep(10)
                                if len(browser.window_handles) > 2:
                                    isChecked = True
                                    startChecking = 0
                                    while 'DO NOT CLOSE THE PAGE' in browser.title or 'YOUHOO' in browser.title:
                                        time.sleep(1)
                                        if 'Checking your view' in browser.title:
                                            if startChecking == 0:
                                                startChecking = datetime.now().timestamp()
                                            elif datetime.now().timestamp() > startChecking + 30:
                                                isChecked = False
                                    if isChecked:
                                        time.sleep(10)
                                        closeOthers_Path(browser, app_path)
                                        browser.switch_to.window(main_window)
                                        log.screen_n_file('[+] Completed Surf ads ₽ task.')
                                        time.sleep(10)
                                    else:
                                        closeOthers_Path(browser, app_path)
                                        browser.switch_to.window(main_window)
                                        get(browser, browser.current_url)
                            elif 'You have watched all the websites' in browser.page_source:
                                time.sleep(10)
                                break
                            elif 'title="reCAPTCHA"' in browser.page_source:
                                while True:
                                    try:
                                        time.sleep(0.2)
                                        if autoCaptcha:
                                            log.screen_n_file('[+] Automatically solve captcha.')
                                            recaptcha = browser.find_element_by_xpath(
                                                "//iframe[contains(@title, 'reCAPTCHA')]")
                                            sitekey = ''
                                            for query in urlparse.urlparse(recaptcha.get_attribute('src')).query.split(
                                                    '&'):
                                                if 'k=' in str(query):
                                                    sitekey = str(query).split('=')[1]
                                            token = ac.reCaptcha(sitekey, browser.current_url)
                                            log.screen_n_file(
                                                '  [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))

                                            # Run callback function
                                            browser.execute_script('''
                                                document.getElementById("g-recaptcha-response").innerHTML=arguments[0];
                                            ''', token)
                                            time.sleep(1)
                                            browser.find_element_by_xpath("//input[contains(@type, 'submit')]").click()
                                            time.sleep(10)
                                            break
                                        else:
                                            log.screen_n_file('[+] Manually solve captcha.')
                                            notification.sound()
                                            notification.notify(app, 'Please solve captcha!')
                                            time.sleep(60)
                                            break
                                    except:
                                        pass
                            elif 'widget containing checkbox for hCaptcha security challenge' in browser.page_source:
                                while True:
                                    try:
                                        time.sleep(0.2)
                                        if autoCaptcha:
                                            log.screen_n_file('  [+] Automatically solve captcha.')
                                            hcaptcha = browser.find_element_by_xpath(
                                                "//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")
                                            sitekey = ''
                                            for fragment in urlparse.urlparse(
                                                    hcaptcha.get_attribute('src')).fragment.split(
                                                '&'):
                                                if 'sitekey=' in str(fragment):
                                                    sitekey = str(fragment).split('=')[1]
                                                    break
                                            token = ac.HCaptcha(sitekey, browser.current_url)
                                            log.screen_n_file(
                                                '    [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))
                                            browser.execute_script('''
                                                document.getElementsByTagName("textarea")[0].innerHTML = arguments[0];
                                                document.getElementsByTagName("form")[0].submit();
                                            ''', token)
                                            time.sleep(10)
                                            break
                                        else:
                                            log.screen_n_file('[+] Manually solve captcha.')
                                            notification.sound()
                                            notification.notify(app, 'Please solve captcha!')
                                            time.sleep(60)
                                            break
                                    except:
                                        pass
                        except:
                            pass

                    # Surf ads
                    link = browser.find_elements_by_xpath("//a[contains(text(), 'Surf ads')]")[1].get_attribute('href')
                    get(browser, link)
                    time.sleep(10)
                    browser.switch_to.window(main_window)
                    while True:
                        try:
                            time.sleep(0.2)
                            if '0pen' in browser.page_source or 'Opеn' in browser.page_source:
                                while True:
                                    detect_string = '0pen'
                                    if 'Opеn' in browser.page_source:
                                        detect_string = 'Opеn'
                                    open_btns = browser.find_elements_by_xpath(
                                        "//a[contains(text(), '" + detect_string + "')]")
                                    for open_btn in open_btns:
                                        try:
                                            open_btn.click()
                                        except:
                                            pass
                                    time.sleep(0.2)
                                    if len(browser.window_handles) > 2:
                                        break
                                time.sleep(10)
                                if len(browser.window_handles) > 2:
                                    isChecked = True
                                    startChecking = 0
                                    while 'DO NOT CLOSE THE PAGE' in browser.title or 'YOUHOO' in browser.title:
                                        time.sleep(1)
                                        if 'Checking your view' in browser.title:
                                            if startChecking == 0:
                                                startChecking = datetime.now().timestamp()
                                            elif datetime.now().timestamp() > startChecking + 30:
                                                isChecked = False
                                    if isChecked:
                                        time.sleep(10)
                                        closeOthers_Path(browser, app_path)
                                        browser.switch_to.window(main_window)
                                        log.screen_n_file('[+] Completed Surf ads task.')
                                        time.sleep(10)
                                    else:
                                        closeOthers_Path(browser, app_path)
                                        browser.switch_to.window(main_window)
                                        get(browser, browser.current_url)
                            elif 'You have watched all the websites' in browser.page_source:
                                time.sleep(10)
                                break
                            elif 'title="reCAPTCHA"' in browser.page_source:
                                while True:
                                    try:
                                        time.sleep(0.2)
                                        if autoCaptcha:
                                            log.screen_n_file('[+] Automatically solve captcha.')
                                            recaptcha = browser.find_element_by_xpath(
                                                "//iframe[contains(@title, 'reCAPTCHA')]")
                                            sitekey = ''
                                            for query in urlparse.urlparse(recaptcha.get_attribute('src')).query.split(
                                                    '&'):
                                                if 'k=' in str(query):
                                                    sitekey = str(query).split('=')[1]
                                            token = ac.reCaptcha(sitekey, browser.current_url)
                                            log.screen_n_file(
                                                '  [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))

                                            # Run callback function
                                            browser.execute_script('''
                                                document.getElementById("g-recaptcha-response").innerHTML=arguments[0];
                                            ''', token)
                                            time.sleep(1)
                                            browser.find_element_by_xpath("//input[contains(@type, 'submit')]").click()
                                            time.sleep(10)
                                            break
                                        else:
                                            log.screen_n_file('[+] Manually solve captcha.')
                                            notification.sound()
                                            notification.notify(app, 'Please solve captcha!')
                                            time.sleep(60)
                                            break
                                    except:
                                        pass
                            elif 'widget containing checkbox for hCaptcha security challenge' in browser.page_source:
                                while True:
                                    try:
                                        time.sleep(0.2)
                                        if autoCaptcha:
                                            log.screen_n_file('  [+] Automatically solve captcha.')
                                            hcaptcha = browser.find_element_by_xpath(
                                                "//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")
                                            sitekey = ''
                                            for fragment in urlparse.urlparse(
                                                    hcaptcha.get_attribute('src')).fragment.split(
                                                '&'):
                                                if 'sitekey=' in str(fragment):
                                                    sitekey = str(fragment).split('=')[1]
                                                    break
                                            token = ac.HCaptcha(sitekey, browser.current_url)
                                            log.screen_n_file(
                                                '    [+] Captcha response is %s.' % (token[:7] + '...' + token[-7:]))
                                            browser.execute_script('''
                                                document.getElementsByTagName("textarea")[0].innerHTML = arguments[0];
                                                document.getElementsByTagName("form")[0].submit();
                                            ''', token)
                                            time.sleep(10)
                                            break
                                        else:
                                            log.screen_n_file('[+] Manually solve captcha.')
                                            notification.sound()
                                            notification.notify(app, 'Please solve captcha!')
                                            time.sleep(60)
                                            break
                                    except:
                                        pass
                        except:
                            pass
                except:
                    pass
        except Exception as ex:
            log.screen_n_file('[!] %s has exception: %s!' % (app, ex))
            notification.notify(app, '%s has exception: %s!' % (app, ex))
        finally:
            browser.quit()


if update.check():
    log.screen_n_file('[*] New version is released. Please download it! Thank you.')
    notification.notify(app, 'New version is released. Please download it! Thank you.')
    os.system('start https://www.youtube.com/watch?v=ymBPf4WaeyE')
else:
    Surfer()
