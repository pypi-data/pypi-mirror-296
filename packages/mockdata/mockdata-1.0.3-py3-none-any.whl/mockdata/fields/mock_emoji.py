from mockdata.init import Common


class MockEmoji(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_emoji(self):
        """随机获取emoji"""
        return self.fake.emoji()



