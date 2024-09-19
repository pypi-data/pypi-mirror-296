from mockdata.init import Common


class MockPython(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_pydict(self):
        """随机字典"""
        return self.fake.pydict()

    def mock_pydecimal(self):
        """随机小数"""
        return self.fake.pydecimal()

    def mock_pyfloat(self):
        """随机浮点数"""
        return self.fake.pyfloat()

    def mock_pyint(self):
        """随机整数"""
        return self.fake.pyint()

    def mock_pylist(self):
        """随机列表"""
        return self.fake.pylist()

    def mock_pyset(self):
        """随机集合"""
        return self.fake.pyset()

    def mock_pystr(self):
        """随机字符串"""
        return self.fake.pystr()

    def mock_pystruct(self):
        """随机结构体"""
        return self.fake.pystruct()

    def mock_pytuple(self):
        """随机元组"""
        return self.fake.pytuple()
