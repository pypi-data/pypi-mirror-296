import markdown

class TestLowerCaseLetterList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_start_default(self):
        text = 'i. List item\nii. List item'
        expected = '<ol type="i">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_ii(self):
        text = 'ii. List item\niii. List item'
        expected = '<ol start="2" type="i">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_all_i(self):
        text = 'i. List item\ni. List item\ni. List item'
        expected = '<ol type="i">\n<li>List item</li>\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected


    def test_start_x(self):
        text = 'x. List item\ni. List item'
        expected = '<ol start="10" type="i">\n<li>List item</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected
