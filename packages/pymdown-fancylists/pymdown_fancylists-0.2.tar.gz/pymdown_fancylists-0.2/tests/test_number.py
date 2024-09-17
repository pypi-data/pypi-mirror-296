import markdown

class TestNumberedList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_start_default(self):
        text = "1. List item\n2. List item"
        expected = "<ol>\n<li>List item</li>\n<li>List item</li>\n</ol>"

        result = self.md.convert(text)

        assert result == expected


    def test_start_2(self):
        text = "2. List item\n3. List item"
        expected = "<ol start=\"2\">\n<li>List item</li>\n<li>List item</li>\n</ol>"

        result = self.md.convert(text)

        assert result == expected


    def test_all_1(self):
        text = "1. List item\n1. List item\n1. List item"
        expected = "<ol>\n<li>List item</li>\n<li>List item</li>\n<li>List item</li>\n</ol>"

        result = self.md.convert(text)

        assert result == expected
