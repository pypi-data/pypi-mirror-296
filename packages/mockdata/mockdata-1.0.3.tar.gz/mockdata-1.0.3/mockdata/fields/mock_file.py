from mockdata.init import Common


class MockFile(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_file_extension(self, category=None):
        """文件后缀
        :category: str
        category有效类别：'audio'、'image'、'office'、 'text'和'video'
        """
        return self.fake.file_extension(category)

    def mock_file_name(self):
        """文件名"""
        return self.fake.file_name()

    def mock_file_path(self):
        """文件路径"""
        return self.fake.file_path()

    def mock_mime_type(self,category=None):
        """文件类型
        如果category是， None则将使用随机类别。
        有效类别列表包括'application'、'audio'、'image'、 'message'、'model'、'multipart'和'text','video'
        """
        return self.fake.mime_type(category)


