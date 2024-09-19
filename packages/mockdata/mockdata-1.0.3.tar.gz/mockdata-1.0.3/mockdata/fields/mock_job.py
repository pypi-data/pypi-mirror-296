from mockdata.init import Common


class MockJob(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_job(self):
        """工作"""
        return self.fake.job()



