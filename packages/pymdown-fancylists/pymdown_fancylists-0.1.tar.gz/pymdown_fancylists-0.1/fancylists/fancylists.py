from markdown import Extension
from markdown.blockprocessors import OListProcessor
from markdown.blockparser import BlockParser
from lxml import etree
import re


def letter_index_to_number(index, reference):
    count = 0
    for letter in index:
        count *= 26
        count += ord(letter) - ord(reference) + 1
    return count


def lower_letter_to_number(letter):
    return letter_index_to_number(letter, 'a')


def upper_letter_to_number(letter):
    return letter_index_to_number(letter, 'A')


class FancylistsProcessor(OListProcessor):
    def __init__(self, parser: BlockParser):
        super().__init__(parser)

        self.RE = re.compile(r'^[ ]{0,%d}([0-9a-zA-Z]+)\.[ ]+(.*)' % (self.tab_length - 1))

        self.CHILD_RE = re.compile(r'^[ ]{0,%d}(([0-9a-zA-Z]+\.)|[*+-])[ ]+(.*)' %
                                   (self.tab_length - 1))

        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}(([0-9a-zA-Z]+\.)|[*+-])[ ]+.*' %
                                    (self.tab_length, self.tab_length * 2 - 1))

        self.TYPE = "1"

        self.LAZY_OL = False


    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        super().run(parent, blocks)

        lst = parent.find('.//ol')

        if self.TYPE != "1":
           lst.set('type', self.TYPE)


    def get_items(self, block: str) -> list[str]:
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
                        if index_match.group('number'):
                            self.TYPE = "1"
                            self.STARTSWITH = index_match.group()
                        elif index_match.group('lower_letter'):
                            self.TYPE = "a"
                            self.STARTSWITH = str(lower_letter_to_number(index_match.group()))
                        elif index_match.group('upper_letter'):
                            self.TYPE = "A"
                            self.STARTSWITH = str(upper_letter_to_number(index_match.group()))

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
