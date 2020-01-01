from typing import Optional, Union

import re

T = Union[int, str]


class Version:

    _exp = re.compile(
        r'''^(?P<major>[0-9]+)
                          \.
                          (?P<minor>[0-9]+)
                          \.
                          (?P<patch>[0-9]+)
                          (-(?P<pre_release>([0-9a-z]+(\.[0-9a-z]+)*)))?$''',
        re.X,
    )

    __slots__ = ('major', 'minor', 'patch', 'pre_release')

    @classmethod
    def from_string(cls, s: str) -> 'Version':
        match = re.match(cls._exp, s)
        if match is None:
            raise ValueError(f'value : {s} cannot be interepreted as a semantic version.')
        return cls(**match.groupdict())

    def __init__(self, major: T = 0, minor: T = 0, patch: T = 0, pre_release: Optional[str] = None):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)
        self.pre_release = pre_release

    def __str__(self) -> str:
        base = f'{self.major}.{self.minor}.{self.patch}'
        if self.pre_release:
            return f'{base}-{self.pre_release}'
        return base

    def __repr__(self) -> str:
        base = (
            f'{self.__class__.__name__}(major={self.major}, minor={self.minor}, patch={self.patch}'
        )
        if self.pre_release:
            return f'{base}, pre_release={self.pre_release})'
        return f'{base})'


class Patch(Version):

    def __init__(self, pre_release: Optional[str] = None):
        super().__init__(patch=1, pre_release=pre_release)

    def __radd__(self, other: Version) -> Version:
        return Version(
            other.major, other.minor, other.patch + self.patch, pre_release=self.pre_release
        )


class Minor(Version):

    def __init__(self, pre_release: Optional[str] = None):
        super().__init__(minor=1, pre_release=pre_release)

    def __radd__(self, other: Version) -> Version:
        return Version(other.major, minor=other.minor + self.minor, pre_release=self.pre_release)


class Major(Version):

    def __init__(self, pre_release: Optional[str] = None):
        super().__init__(major=1, pre_release=pre_release)

    def __radd__(self, other: Version) -> Version:
        return Version(major=self.major + other.major, pre_release=self.pre_release)


class Release(Version):

    def __init__(self):
        super().__init__()

    def __radd__(self, other: Version) -> Version:
        return Version(other.major, other.minor, other.patch, pre_release=None)
