from mockdata.init import Common


class MockGeo(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_latitude(self):
        """mock latitude(维度)"""
        return self.fake.latitude()

    def mock_longitude(self):
        """mock longitude(经度)"""
        return self.fake.longitude()

