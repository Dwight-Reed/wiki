from bleach import Cleaner
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.preprocessors import Preprocessor
import xml.etree.ElementTree as etree
from .models import Entry


# List copied from https://community.fandom.com/wiki/Help:HTML
ALLOWED_TAGS = ["abbr", "b", "bdi", "bdo", "blockquote", "br", "caption", "cite", "code", "data", "dd", "del", "dfn", "div", "dl", "dt", "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "ins", "kbd", "li", "mark", "ol", "p", "pre", "q", "rp", "rt", "ruby", "s", "samp", "small", "span", "strong", "sub", "sup", "table", "td", "th", "time", "tr", "u", "ul", "var", "wbr"]


class WikiSyntax(Extension):
    def extendMarkdown(self, md):
        pattern = r"(\[\[)([^\[\]]*)(\]\])"

        # No priority requirements
        md.inlinePatterns.register(EntryLink(pattern, md), "wiki_link", 175)

        # Most load after fenced_code_block (25), and before html_block (20)
        md.preprocessors.register(BleachPreprocessor(md), "bleach_preprocessor", 23)


# replace [[entry_title]] with a link to the corresponding page
class EntryLink(InlineProcessor):
    def handleMatch(self, m, data):
        link = etree.Element("a")
        link.set("href", reverse("wiki", args={m.group(2)}))
        link.set("class", "entry-link")
        try:
            Entry.objects.get(title=m.group(2))

        except ObjectDoesNotExist:
            link.attrib["class"] += " broken-link"

        link.text = m.group(2)

        return link, m.start(0), m.end(0)


# Escapes any html tags not in ALLOWED_TAGS
class BleachPreprocessor(Preprocessor):
    cleaner = Cleaner(tags=ALLOWED_TAGS)

    def run(self, lines):
        text = "\n".join(lines)
        cleaned_text = self.cleaner.clean(text)
        return cleaned_text.splitlines()
