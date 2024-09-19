import json
import random

from mockdata.init import Common


class MockCreditCard(Common):
    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()
        # 自定义银行列表
        self.bank = {
            "bank": [
                "中国银行",
                "工商银行",
                "建设银行",
                "农业银行",
                "招商银行",
                "交通银行",
                "民生银行",
                "华夏银行",
                "浦发银行",
                "中信银行",
                "光大银行",
                "广发银行",
                "平安银行",
                "北京银行",
                "上海银行",
                "南京银行",
                "杭州银行",
                "宁波银行",
                "广州银行",
                "深圳发展银行",
                "浙商银行",
                "渤海银行",
                "恒丰银行",
                "邮政储蓄银行",
                "汇丰银行",
                "花旗银行",
                "渣打银行",
                "东亚银行",
                "大华银行",
                "星展银行",
                "汇丰银行（中国）有限公司",
                "东亚银行（中国）有限公司",
                "恒生银行"
            ]
        }

    def mock_credit_card_expire(self):
        """生成信用卡到期日期"""
        return self.fake.credit_card_expire()

    def mock_credit_card_full(self):
        """生成信用卡详细信息"""
        return self.fake.credit_card_full()

    def mock_credit_card_number(self):
        """生成信用卡卡号"""
        return self.fake.credit_card_number()

    def mock_credit_card_provider(self):
        """生成信用卡提供者"""
        banks_list = self.bank["bank"]
        return random.choice(banks_list)

    def mock_credit_card_security_code(self):
        """生成信用卡安全码"""
        return self.fake.credit_card_security_code()
