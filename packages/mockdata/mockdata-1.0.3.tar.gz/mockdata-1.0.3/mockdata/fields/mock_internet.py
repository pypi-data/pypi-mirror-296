from mockdata.init import Common


class MockInternet(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_company_email(self):
        """Mock ascii_email"""
        return self.fake.company_email()

    def mock_email(self):
        """Mock email"""
        return self.fake.ascii_email()

    def mock_domain_name(self):
        """Mock domain_name"""
        return self.fake.domain_name()

    def mock_http_method(self):
        """Mock http_method"""
        return self.fake.http_method()

    def mock_http_status_code(self):
        """Mock http_status_code"""
        return self.fake.http_status_code()

    def mock_image_url(self):
        """Mock image_url"""
        return self.fake.image_url()

    def mock_ipv4(self):
        """Mock ipv4"""
        return self.fake.ipv4()

    def mock_ipv6(self):
        """Mock ipv6"""
        return self.fake.ipv6()

    def mock_port_number(self):
        """Mock port_number"""
        return self.fake.port_number()

    def mock_uri(self):
        """Mock uri"""
        return self.fake.uri()

    def mock_url(self):
        """Mock url"""
        return self.fake.url()

    def mock_user_name(self):
        """Mock user_name"""
        return self.fake.user_name()



