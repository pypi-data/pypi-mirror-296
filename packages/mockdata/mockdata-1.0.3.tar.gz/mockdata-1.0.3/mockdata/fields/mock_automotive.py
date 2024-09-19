from mockdata.init import Common


class MockAutomotive(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_license_plate(self):
        """汽车车牌号"""
        return self.fake.license_plate()  # 桂A-61102

    def mock_vin(self):
        """车辆识别码"""
        return self.fake.vin()  # SMS2BR3057U7WNFEL



