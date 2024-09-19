from mockdata.init import Common


class MockProfile(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_profile(self):
        """个人信息（详细）"""
        return self.fake.profile()

    def mock_simple_profile(self):
        """个人信息（简介）"""
        return self.fake.simple_profile()


