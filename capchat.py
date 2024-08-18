import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from twocaptcha import TwoCaptcha


api_key = "096419e695f63b10a824c1774697408d"
solver = TwoCaptcha(api_key)

try:
    result = solver.recaptcha(
        sitekey='6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u',
        url='https://v5.voiranime.com/anime/dead-dead-demons-dededede-destruction/dead-dead-demons-dededede-destruction-12-vostfr/')

except Exception as e:
    sys.exit(e)

else:
    sys.exit('solved: ' + str(result))
# config = {
#             'server':           '2captcha.com',
#             'apiKey':           'YOUR_API_KEY',
#             'softId':            123,
#             'callback':         'https://your.site/result-receiver',
#             'defaultTimeout':    120,
#             'recaptchaTimeout':  600,
#             'pollingInterval':   10,
#         }
# data-sitekey="6Lfd5wobAAAAACjTkOIXohTrPz9RIhNwRqRq2_R9"
# solver = TwoCaptcha(**config)