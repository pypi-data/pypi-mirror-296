from mockdata.init import Common
import base64

from mockdata.utils.convert import base64_to_image


class MockMisc(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_binary(self):
        """Mock binary data"""
        return self.fake.binary()

    def mock_csv(self):
        """Mock csv data"""
        return self.fake.csv()

    def mock_fixed_width(self):
        """Mock fixed width data"""
        return self.fake.fixed_width()

    def mock_image(self, path='../img/image.png'):
        """随机生成图片并保存到指定路径"""
        bytes_str = self.fake.image()  # 二进制
        base64_str = base64.b64encode(bytes_str)
        base64_to_image(base64_str, path)
        return '图片保存位置:{}'.format(path)

    def mock_json(self):
        """Mock json data"""
        return self.fake.json()

    def mock_md5(self):
        """Mock md5 data"""
        return self.fake.md5()

    def mock_password(self):
        """Mock password data"""
        return self.fake.password()

    def mock_uuid4(self):
        """Mock uuid4 data"""
        return self.fake.uuid4()
