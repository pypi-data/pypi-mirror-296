from mockdata.init import Common


class MockAddress(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_address(self):
        """随机获取地址"""
        return self.fake.address()  # 安徽省太原县城北哈尔滨街n座 645024

    def mock_building_number(self):
        """随机获取楼栋"""
        return self.fake.building_number()  # J座

    def mock_city(self):
        """随机获取城市"""
        return self.fake.city()  # 青岛市

    def mock_country(self):
        """随机获取国家"""
        return self.fake.country()  # 阿尔巴尼亚

    def mock_postcode(self):
        """随机获取邮编"""
        return self.fake.postcode()  # 645024

    def mock_street_address(self):
        """随机获取街道"""
        return self.fake.street_address()

    def mock_street_name(self):
        """随机获取街道名"""
        return self.fake.street_name()

    def mock_street_suffix(self):
        """随机获取街道后缀"""
        return self.fake.street_suffix()

    def mock_city_suffix(self):
        """随机获取城市后缀"""
        return self.fake.city_suffix()

    def mock_country_code(self):
        """随机获取国家代码"""
        return self.fake.country_code()

    def mock_current_country_code(self):
        """随机获取当前国家代码"""
        return self.fake.current_country_code()


