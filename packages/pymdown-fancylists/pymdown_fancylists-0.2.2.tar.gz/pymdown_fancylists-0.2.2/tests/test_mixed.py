import markdown

class TestMixedList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_mixed(self):
        text = '2. List item\n3. List item\n  a. List item\n    b. List item\n    v. List item\n    vi. List item\n4. List item'
        expected = '<ol start="2">\n<li>List item</li>\n<li>List item\n<ol type="a">\n<li>List item</li>\n<li>List item\n<ol type="i">\n<li>List item</li>\n<li>List item</li>\n</ol>\n</li>\n</ol>\n</li>\n<li>List item</li>\n</ol>'

        result = self.md.convert(text)

        assert result == expected
