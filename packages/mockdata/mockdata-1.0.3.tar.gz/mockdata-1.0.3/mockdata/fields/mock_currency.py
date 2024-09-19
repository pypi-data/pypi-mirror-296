from mockdata.init import Common


class MockCurrency(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_cryptocurrency(self):
        """加密货币"""
        return self.fake.cryptocurrency()

    def mock_cryptocurrency_code(self):
        """加密货币代码"""
        return self.fake.cryptocurrency_code()

    def mock_cryptocurrency_name(self):
        """加密货币名称"""
        return self.fake.cryptocurrency_name()

    def mock_currency(self):
        """货币"""
        return self.fake.currency()

    def mock_currency_code(self):
        """货币代码"""
        return self.fake.currency_code()

    def mock_currency_name(self):
        """货币名称"""
        return self.fake.currency_name()

    def mock_currency_symbol(self):
        """货币符号"""
        return self.fake.currency_symbol()

    def mock_pricetag(self):
        """价格标签"""
        return self.fake.pricetag()


