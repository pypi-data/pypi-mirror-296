import markdown

class TestUpperCaseLetterList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_start_default(self):
        text = 'A. List item\nB. List item'
        expected = '<ol type="A">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_B(self):
        text = 'B. List item\nC. List item'
        expected = '<ol start="2" type="A">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_all_A(self):
        text = 'A. List item\nA. List item\nA. List item'
        expected = '<ol type="A">\n<li>List item</li>\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_AA(self):
        text = 'AA. List item\nAB. List item'
        expected = '<ol start="27" type="A">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_ZZ(self):
        text = 'ZZ. List item\nAAA. List item'
        expected = '<ol start="702" type="A">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected
