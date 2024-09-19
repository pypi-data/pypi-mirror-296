from mockdata.init import Common


class MockPassport(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_passport_number(self):
        """随机护照号码"""
        return self.fake.passport_number()

    def mock_passport_owner(self):
        """随机护照持有人"""
        return self.fake.passport_owner()



