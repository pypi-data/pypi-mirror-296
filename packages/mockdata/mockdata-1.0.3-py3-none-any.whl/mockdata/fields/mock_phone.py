from mockdata.init import Common


class MockPhone(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_country_calling_code(self):
        """国家呼叫代码"""
        return self.fake.country_calling_code()

    def mock_msisdn(self):
        """摩斯登密码"""
        return self.fake.msisdn()

    def mock_phone_number(self):
        """电话号码"""
        return self.fake.phone_number()



