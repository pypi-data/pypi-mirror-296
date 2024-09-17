import markdown

class TestMixedList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_2_depth(self):
        text = (
            '1. List item\n'
            '2. List item\n'
            '    a. List item\n'
            '    b. List item\n'
            '3. List item'
        )

        expected = (
            '<ol>\n'
            '<li>List item</li>\n'
            '<li>List item'
            '<ol type="a">\n'
            '<li>List item</li>\n'
            '<li>List item</li>\n'
            '</ol>\n' # end type="a"
            '</li>\n'
            '<li>List item</li>\n'
            '</ol>' # end type="1"
        )

        result = self.md.convert(text)

        assert result == expected

    def test_3_depth(self):
        text = (
            '2. List item\n'
            '3. List item\n'
            '    a. List item\n'
            '    b. List item\n'
            '        v. List item\n'
            '        vi. List item\n'
            '4. List item'
        )

        expected = (
            '<ol start="2">\n'
            '<li>List item</li>\n'
            '<li>List item'
            '<ol type="a">\n'
            '<li>List item</li>\n'
            '<li>List item'
            '<ol start="5" type="i">\n'
            '<li>List item</li>\n'
            '<li>List item</li>\n'
            '</ol>\n' # end type="i"
            '</li>\n'
            '</ol>\n' # end type="a"
            '</li>\n'
            '<li>List item</li>\n'
            '</ol>' # end type="1"
        )

        result = self.md.convert(text)

        assert result == expected
