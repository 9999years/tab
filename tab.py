import itertools
import re
from dataclasses import dataclass
import argparse
import sys
from typing import List, Text, Iterable, Union, Generator, Any, Iterator

# split on two or more spaces
SPACES_PATTERN = re.compile(' {2,}')
# this is actually just a plain string...
TABS_PATTERN = re.compile('\t')


@dataclass
class Splitter:
    pat: re.Pattern = None

    def split(self, line):
        if self.pat is None:
            if '\t' in line:
                self.pat = TABS_PATTERN
            else:
                self.pat = SPACES_PATTERN
        return self.pat.split(line)

    def join(self, fields: Iterable[Text]) -> Text:
        joiner = '\t' if self.pat is TABS_PATTERN else '  '
        return joiner.join(fields)


class Fields:
    """
    a range of fields; '2' would be the single field 2 and '3-5' would be fields '3-5' (inclusive)
    """
    bottom: int
    top: int

    def __init__(self, txt: Text):
        if '-' in txt:
            self.bottom, self.top = map(int, txt.split('-'))
        else:
            self.bottom = self.top = int(txt)
        self.top += 1

    def __iter__(self):
        return (n for n in range(self.bottom, self.top))


class FieldList:
    fields: List[Fields]

    def __init__(self, fieldspecs: Union[Iterable[Text], Iterable[Fields]]):
        self.fields = list()
        for spec in fieldspecs:
            if isinstance(spec, Text):
                self.fields.append(Fields(spec))
            else:
                self.fields.append(spec)

    # lazy concat
    def __iter__(self) -> Iterator[int]:
        return (n for n in itertools.chain(*self.fields))


@dataclass
class FieldGetter:
    fields: Iterable[int]

    def get(self, items: Iterable[Any]) -> List[Any]:
        field_iter = iter(self.fields)

        def maybe_next():
            try:
                return next(field_iter)
            except StopIteration:
                return None

        next_field = maybe_next()
        ret = []
        for i, item in enumerate(items):
            if next_field is None:
                return ret
            if i == next_field:
                ret.append(item)
                next_field = maybe_next()

        return ret


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('fields', nargs='+', type=Fields)
    return parser


def main():
    parser = argparser()
    args = parser.parse_args()
    fieldgetter = FieldGetter(FieldList(args.fields))
    splitter = Splitter()
    for line in sys.stdin:
        split = splitter.split(line)
        filtered = fieldgetter.get(split)
        print(splitter.join(filtered))


if __name__ == '__main__':
    main()
