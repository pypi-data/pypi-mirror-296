# 创建基类common，实例化faker
from faker import Faker


class Common:

    def __init__(self, lan='zh_CN'):
        self.fake = Faker(lan)

    def get_fake(self):
        return self.fake
