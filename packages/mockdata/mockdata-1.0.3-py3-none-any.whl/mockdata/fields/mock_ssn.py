from mockdata.init import Common


class MockSsn(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_ssn(self):
        """ Mock a social security number
        在美国，社会安全号码（Social Security number，SSN）是发给公民、
        永久居民、临时（工作）居民的一组九位数字号码，
        是依据美国社会安全法案（Social Security Act）205条C2中社会安全卡的记载。
        这组数字由联邦政府社会安全局针对个人发行。社会安全号码主要的目的是为了追踪个人的赋税资料，
        但近年来已经成为实际上（De facto）的国民辨识号码。
        社会安全号码可利用SS–5申请表格获得，是依据联邦法令集第20章422条103项b的记载。
        """
        return self.fake.ssn()



