import unittest
from recaptcha_bypass import ReCaptchaEnterpriseV2Bypass

class TestReCaptchaEnterpriseV2Bypass(unittest.TestCase):

    def test_bypass(self):
        # Replace with an actual URL for testing
        target_url = "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeO36obAAAAALSBZrY6RYM1hcAY7RLvpDDcJLy3&co=aHR0cHM6Ly9jaGFsbGVuZ2Uuc3BvdGlmeS5jb206NDQz&hl=en&v=EGbODne6buzpTnWrrBprcfAY&theme=dark&size=normal&sa=challenge&cb=wpnigaiaxwgv"
        bypass = ReCaptchaEnterpriseV2Bypass(target_url)
        recaptcha_token = bypass.bypass()
        self.assertIsNotNone(recaptcha_token, "Token Alınamadı")

if __name__ == '__main__':
    unittest.main()