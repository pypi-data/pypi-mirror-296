from mockdata.init import Common


class MockLorem(Common):

    def __init__(self, lan='zh_CN'):
        super().__init__(lan)
        self.fake = self.get_fake()

    def mock_get_words_list(self):
        return self.fake.get_words_list()

    def mock_paragraph(self):
        return self.fake.paragraph()

    def mock_paragraphs(self, num=1):
        return self.fake.paragraphs(nb=num)

    def mock_sentence(self, num=1):
        return self.fake.sentence(nb_words=num)

    def mock_sentences(self):
        return self.fake.sentences()

    def mock_text(self, max_nb_chars=200, ext_word_list=None):
        return self.fake.text(max_nb_chars=max_nb_chars, ext_word_list=ext_word_list)

    def mock_texts(self, max_nb_chars=400, ext_word_list=None):
        return self.fake.texts(max_nb_chars=max_nb_chars, ext_word_list=ext_word_list)

    def mock_word(self):
        return self.fake.word()

    def mock_words(self, nb=3):
        return self.fake.words(nb=nb)
