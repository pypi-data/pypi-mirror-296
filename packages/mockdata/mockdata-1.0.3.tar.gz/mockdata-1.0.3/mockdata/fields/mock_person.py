from mockdata.init import Common


class MockPerson(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_first_name(self):
        """随机名字"""
        return self.fake.first_name()

    def mock_last_name(self):
        """随机姓氏"""
        return self.fake.last_name()

    def mock_full_name(self):
        """随机全名"""
        return self.fake.name()

    def mock_first_name_female(self):
        """随机女性名字"""
        return self.fake.first_name_female()

    def mock_first_name_male(self):
        """随机男性名字"""
        return self.fake.first_name_male()

    def mock_language_name(self):
        """随机语言名称"""
        return self.fake.language_name()

    def mock_name_female(self):
        """随机女性全名"""
        return self.fake.name_female()

    def mock_name_male(self):
        """随机男性全名"""
        return self.fake.name_male()



