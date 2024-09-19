from mockdata.init import Common


class MockCompany(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_company(self):
        """Acme 有限公司"""
        return self.fake.company()

    def mock_company_suffix(self):
        """有限公司"""
        return self.fake.company_suffix()



