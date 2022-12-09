import bleach
import re

from itertools import chain


# htmlStash from markdown.util adds invisible characters (\x02 and \x03) surrounding the placeholder string that can't be removed,
# bleach.sanitizer.Cleaner removes invisible characters, but does not have a config for specifying these;
# therefore, it must be redefined here
INVISIBLE_CHARACTERS = "".join(
    [chr(c) for c in chain([0, 1], range(4, 9), range(11, 13), range(14, 32))]
)

bleach.sanitizer.INVISIBLE_CHARACTERS_RE = re.compile("[" + INVISIBLE_CHARACTERS + "]", re.UNICODE)
