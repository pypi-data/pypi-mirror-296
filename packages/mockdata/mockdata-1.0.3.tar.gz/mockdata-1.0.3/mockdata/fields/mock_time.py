import datetime

from mockdata.init import Common


class MockTime(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_date_time(self):
        """随机获取日期时间"""
        _date_time = self.fake.date_time()  # .strftime('%Y-%m-%d %H:%M:%S') 2017-04-22 01:43:35
        return _date_time

    def mock_date(self):
        """随机获取日期"""
        date = self.fake.date()  # .strftime('%Y-%m-%d') 2017-04-22
        return date

    def mock_time(self):
        """随机获取时间"""
        time = self.fake.time()  # .strftime('%H:%M:%S') 01:43:35
        return time

    def mock_year(self):
        """随机获取年份"""
        year = self.fake.year()  # .strftime('%Y') 2017
        return year

    def mock_month(self):
        """随机获取月份"""
        month = self.fake.month()  # .strftime('%m-') 04
        return month

    def mock_day(self):
        """随机获取日期数"""
        day = self.fake.day_of_month()  # .strftime('%d') 22
        return day

    def mock_timestamp(self):
        """随机获取时间戳"""
        fake_datetime = self.fake.date_time()
        timestamp = int(datetime.datetime.timestamp(fake_datetime))  # 1492836215.123456
        return timestamp

    def mock_day_of_week(self):
        """随机获取星期几"""
        day_of_week = self.fake.day_of_week()  # 星期几，星期一为1，星期天为7
        return day_of_week

    def mock_future_date(self):
        """随机获取未来日期"""
        future_date = self.fake.future_date()  # .strftime('%Y-%m-%d') 2017-04-22
        return future_date

    def mock_timezone(self):
        """随机获取时区"""
        timezone = self.fake.timezone()  # 'Europe/Andorra'
        return timezone
