from markdown import Extension
from markdown.blockprocessors import OListProcessor
import re


def letter_to_number(index):
    count = 0
    for letter in index:
        count *= 26
        count += ord(letter) - ord('a') + 1
    return count


def roman_to_number(roman):
    roman_map = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}
    result = 0
    prev = 0
    for letter in reversed(roman):
        if letter not in roman_map:
            return None

        value = roman_map[letter]
        if value < prev:
            result -= value
        else:
            result += value
        prev = value
    return result


class FancylistsProcessor(OListProcessor):
    def __init__(self, parser):
        super().__init__(parser)

        self.RE = re.compile(r'^[ ]{0,%d}([0-9a-zA-Z]+)\.[ ]+(.*)' % (self.tab_length - 1))

        self.CHILD_RE = re.compile(r'^[ ]{0,%d}(([0-9a-zA-Z]+\.)|[*+-])[ ]+(.*)' %
                                   (self.tab_length - 1))

        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}(([0-9a-zA-Z]+\.)|[*+-])[ ]+.*' %
                                    (self.tab_length, self.tab_length * 2 - 1))

        self.TYPE = "1"

        self.LAZY_OL = False


    def run(self, parent, blocks):
        super().run(parent, blocks)

        lst = parent.find('.//ol')

        if self.TYPE != "1":
           lst.set('type', self.TYPE)


    def get_items(self, block):
        """ Break a block into list items. """
        items = []
        for line in block.split('\n'):
            m = self.CHILD_RE.match(line)
            if m:
                # This is a new list item
                # Check first item for the start index
                if not items and self.TAG == 'ol':
                    # Detect the integer value of first list item
                    # INDEX_RE = re.compile(r'([0-9a-zA-Z]+)')
                    INDEX_RE = re.compile(r'(?P<number>\d+)|(?P<lower_letter>[a-z]+)|(?P<upper_letter>[A-Z]+)')
                    index_match = INDEX_RE.match(m.group(1))

                    if index_match:
                        index_text = index_match.group()
                        if index_match.group('number'):
                            self.TYPE = "1"
                            self.STARTSWITH = index_text
                        elif index_match.group('lower_letter'):
                            roman_value = roman_to_number(index_text)
                            if roman_value:
                                self.TYPE = "i"
                                self.STARTSWITH = str(roman_value)
                            else:
                                self.TYPE = "a"
                                self.STARTSWITH = str(letter_to_number(index_text))
                        elif index_match.group('upper_letter'):
                            index_text = index_text.lower()
                            roman_value = roman_to_number(index_text)
                            if roman_value:
                                self.TYPE = "I"
                                self.STARTSWITH = str(roman_value)
                            else:
                                self.TYPE = "A"
                                self.STARTSWITH = str(letter_to_number(index_text))

                # Append to the list
                items.append(m.group(3))
            elif self.INDENT_RE.match(line):
                # This is an indented (possibly nested) item.
                if items[-1].startswith(' '*self.tab_length):
                    # Previous item was indented. Append to that item.
                    items[-1] = '{}\n{}'.format(items[-1], line)
                else:
                    items.append(line)
            else:
                # This is another line of previous item. Append to that item.
                items[-1] = '{}\n{}'.format(items[-1], line)
        return items


class FancylistsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(FancylistsProcessor(md.parser), 'fancylist', 50)


def makeExtension(**kwargs):
    """Return extension."""

    return FancylistsExtension(**kwargs)
