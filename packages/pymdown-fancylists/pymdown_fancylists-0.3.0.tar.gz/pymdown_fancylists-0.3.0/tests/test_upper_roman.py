import markdown

class TestLowerCaseLetterList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_start_default(self):
        text = 'I. List item\nII. List item'
        expected = '<ol type="I">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_ii(self):
        text = 'II. List item\nIII. List item'
        expected = '<ol start="2" type="I">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_all_i(self):
        text = 'I. List item\nI. List item\nI. List item'
        expected = '<ol type="I">\n<li>List item</li>\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_x(self):
        text = 'X. List item\nI. List item'
        expected = '<ol start="10" type="I">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected
