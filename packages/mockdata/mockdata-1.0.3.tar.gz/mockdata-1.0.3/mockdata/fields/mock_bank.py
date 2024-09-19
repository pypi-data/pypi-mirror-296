from mockdata.init import Common


class MockBank(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_aba(self):
        """生成 ABA 路由中转号码"""
        return self.fake.aba()  # 105351829

    def mock_bank_country(self):
        """生成银行提供商的 ISO 3166-1 alpha-2 国家代码"""
        return self.fake.country_code()

    def mock_bban(self):
        """生成基本银行账号 (BBAN)"""
        return self.fake.bban()

    def mock_iban(self):
        """生成国际银行账号 (IBAN)"""
        return self.fake.iban()

    def mock_swift(self):
        """
        SWIFT 代码从左到右依次由 4 个字母组成的银行代码、2 个字母组成的国家代码、
        2 个字母数字位置代码和可选的 3 个字母数字分行代码组成。这意味着 SWIFT
        代码只能有 8 个或 11 个字符，因此 的值 length只能是None或整数8或11。
        如果 的值为，则将随机分配或 的None值。811由于所有 8 位 SWIFT 代码都
        已指向主要分支机构或办事处，因此，只有 的值为 时，该参数primary才会生效 。
        如果且 为，则 生成的 11 位 SWIFT 代码将始终以 结尾，
        以表示它们属于主要分支机构/办事处。length11primaryTruelength11'XXX'
        为了提高真实性，本地化提供商可以选择包含其各自区域使用的 SWIFT 银行代码、
        位置代码和分行代码。如果use_dataset是True，此方法将根据这些区域特定的代码（如果包含）
        生成 SWIFT 代码。如果未包含这些代码，则其行为将如同 一样use_dataset，
         False在该模式下，所有这些代码都将根据规范随机生成。
        """
        """生成 SWIFT/BIC 编号"""
        return self.fake.swift()

    def mock_swift11(self):
        """生成 SWIFT/BIC 编号"""
        return self.fake.swift11()

    def mock_swift8(self):
        """生成 SWIFT/BIC 编号"""
        return self.fake.swift8()



