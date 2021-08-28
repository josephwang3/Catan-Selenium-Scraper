import requests

passcode = 'QTS6'

source = requests.get('https://colonist.io/#' + passcode)
print(source.status_code)

param = {"apiKey":"a38719f2-d919-446b-b2e3-0da55a22a29a","eventName":"funnel_game_get_resources","eventUniqueId":"543b6980-e357-4411-d200-d7251d80b193","properties":{"browser":"Chrome","browser_os":"Windows","browser_device":"Web","browser_language":"en-US","page_title":"New Message","page_url":"https://colonist.io/#QTS6"}}

source2 = requests.post('https://api.indicative.com/service/event', data = param)
print(source2.status_code)