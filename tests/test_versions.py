import string
import pytest

from hypothesis import given
from hypothesis import strategies as st
from yabump.version import Version, Patch, Minor, Major, Release

pre_release_tags = st.one_of(
    st.none(),
    st.lists(st.text(string.ascii_lowercase + string.digits, min_size=1), min_size=1).map(
        lambda x: '.'.join(x)
    ),
)

version_ints = st.integers(min_value=0)
version_args = st.fixed_dictionaries(
    {
        'major': version_ints,
        'minor': version_ints,
        'patch': version_ints,
        'pre_release': pre_release_tags,
    }
)


def to_version_str(major, minor, patch, pre_release):
    base = f'{major}.{minor}.{patch}'
    if pre_release is not None:
        return base + '-' + pre_release
    return base


class TestVersion:

    @given(version_args.map(lambda x: to_version_str(**x)))
    def test_from_valid_string(self, s):
        v = Version.from_string(s)
        assert str(v) == s

    @given(st.text())
    def test_from_invalid_string(self, s):
        with pytest.raises(ValueError):
            Version.from_string(s)


versions = st.builds(
    lambda x: Version(**x),
    st.fixed_dictionaries({'major': version_ints, 'minor': version_ints, 'patch': version_ints}),
)


@given(versions)
def test_patch_no_prerelease(version):
    version_str = str(version)
    new_version = version + Patch()
    assert str(version) == version_str
    assert new_version.major == version.major
    assert new_version.minor == version.minor
    assert new_version.patch == version.patch + 1
    assert new_version.pre_release is None


@given(version=versions, pre_release=pre_release_tags)
def test_patch_with_prerelease(version, pre_release):
    version_str = str(version)
    new_version = version + Patch(pre_release)
    assert str(version) == version_str
    assert new_version.major == version.major
    assert new_version.minor == version.minor
    assert new_version.patch == version.patch + 1
    assert new_version.pre_release == pre_release


@given(versions)
def test_minor_no_prerelease(version):
    version_str = str(version)
    new_version = version + Minor()
    assert str(version) == version_str
    assert new_version.major == version.major
    assert new_version.minor == version.minor + 1
    assert new_version.patch == 0
    assert new_version.pre_release is None


@given(version=versions, pre_release=pre_release_tags)
def test_minor_with_prerelease(version, pre_release):
    version_str = str(version)
    new_version = version + Minor(pre_release)
    assert str(version) == version_str
    assert new_version.major == version.major
    assert new_version.minor == version.minor + 1
    assert new_version.patch == 0
    assert new_version.pre_release == pre_release


@given(versions)
def test_major_no_prerelease(version):
    version_str = str(version)
    new_version = version + Minor()
    assert str(version) == version_str
    assert new_version.major == version.major
    assert new_version.minor == version.minor + 1
    assert new_version.patch == 0
    assert new_version.pre_release is None


@given(version=versions, pre_release=pre_release_tags)
def test_major_with_prerelease(version, pre_release):
    version_str = str(version)
    new_version = version + Major(pre_release)
    assert str(version) == version_str
    assert new_version.major == version.major + 1
    assert new_version.minor == 0
    assert new_version.patch == 0
    assert new_version.pre_release == pre_release


@given(version=st.builds(lambda x: Version(**x), version_args))
def test_release(version):
    version_str = str(version)
    new_version = version + Release()
    assert str(version) == version_str
    assert new_version.major == version.major
    assert new_version.minor == version.minor
    assert new_version.patch == version.patch
    assert new_version.pre_release is None
