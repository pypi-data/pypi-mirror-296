import markdown

class TestLowerCaseLetterList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_start_default(self):
        text = 'a. List item\nb. List item'
        expected = '<ol type="a">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_b(self):
        text = 'b. List item\nc. List item'
        expected = '<ol start="2" type="a">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_all_A(self):
        text = 'a. List item\na. List item\na. List item'
        expected = '<ol type="a">\n<li>List item</li>\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_aa(self):
        text = 'aa. List item\nab. List item'
        expected = '<ol start="27" type="a">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_zz(self):
        text = 'zz. List item\naaa. List item'
        expected = '<ol start="702" type="a">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected
