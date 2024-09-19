from mockdata.init import Common


class MockColor(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_color(self):
        return self.fake.color()

    def mock_color_hsl(self):
        """以人性化的方式生成 HSV 颜色元组"""
        return self.fake.color()

    def mock_color_name(self):
        """生成颜色名称"""
        return self.fake.color_name()

    def mock_color_rgb(self):
        """生成 RGB 颜色元组"""
        return self.fake.color_rgb()

    def mock_color_rgb_float(self):
        """以人性化的方式生成浮点数的 RGB 颜色元组"""
        return self.fake.color_rgb_float()

    def mock_hex_color(self):
        """生成十六进制颜色码"""
        return self.fake.hex_color()

    def mock_rgb_color(self):
        """生成 RGB 颜色元组"""
        return self.fake.rgb_color()

    def mock_rgb_css_color(self):
        """生成 RGB CSS 颜色字符串"""
        return self.fake.rgb_css_color()

    def mock_safe_color_name(self):
        """生成网页安全颜色名称"""
        return self.fake.safe_color_name()

    def mock_safe_hex_color(self):
        """生成安全十六进制颜色码"""
        return self.fake.safe_hex_color()


