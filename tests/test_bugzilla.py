from helga_bugzilla import is_ticket, sanitize, get_bug_url, get_bug_subject
import pytest
from bugzilla import BugzillaError


def line_matrix():
    pre_garbage = [' ', '', 'some question about ',]
    prefixes = ['bug', 'BuG', 'bz', 'rhbz', 'RHBZ']
    numbers = ['#123467890', '1234567890']
    garbage = ['?', ' ', '.', '!', '..', '...']
    lines = []

    for pre in pre_garbage:
        for prefix in prefixes:
            for number in numbers:
                for g in garbage:
                    lines.append('%s%s %s%s' % (
                        pre, prefix, number, g
                        )
                    )
    return lines


def fail_line_matrix():
    pre_garbage = [' ', '', 'some question about ',]
    pre_prefixes = ['', ' ', 'f']
    prefixes = ['bugs', 'RHBZ']
    numbers = ['#G123467890', 'F1234567890']
    garbage = ['?', ' ', '.', '!', '..', '...']
    lines = []

    for pre in pre_garbage:
        for pre_prefix in pre_prefixes:
            for prefix in prefixes:
                for number in numbers:
                    for g in garbage:
                        lines.append('%s%s%s %s%s' % (
                            pre, pre_prefix, prefix, number, g
                            )
                        )
    return lines


class TestIsTicket(object):

    @pytest.mark.parametrize('line', line_matrix())
    def test_matches(self, line):
        assert is_ticket(line)

    @pytest.mark.parametrize('line', fail_line_matrix())
    def test_does_not_match(self, line):
        assert is_ticket(line) is None


def match_matrix():
    matches = ['1234', '#1234']
    prefixes = ['', ' ']
    suffixes = ['', ' ']
    lines = []

    for match in matches:
        for prefix in prefixes:
            for suffix in suffixes:
                lines.append(
                    ['', '%s%s%s' % (prefix, match, suffix)]
                )
    return lines


class TestSanitize(object):

    @pytest.mark.parametrize('match', match_matrix())
    def test_sanitizes(self, match):
        assert sanitize(match) == '1234'


class FakeSettings(object):
    pass


class FakeBug(object):
    pass


class TestGetBugUrl(object):

    def test_get_custom_url(self):
        settings = FakeSettings()
        url = "https://bugzilla.example.com/%(ticket)s"
        settings.BUGZILLA_TICKET_URL = url
        bug = FakeBug()
        result = get_bug_url(settings, bug, 1234)
        assert result == 'https://bugzilla.example.com/1234'

    def test_get_fallback_url(self):
        settings = FakeSettings()
        bug = FakeBug()
        bug.weburl = 'https://bugzilla.example.com/show_bug.cgi?id=1234'
        result = get_bug_url(settings, bug, 1234)
        assert result == 'https://bugzilla.example.com/show_bug.cgi?id=1234'

    def test_get_broken_bug_url(self):
        settings = FakeSettings()
        bug = FakeBug()
        bug.__getattr__ = lambda: (_ for _ in ()).throw(BugzillaError('boom'))
        result = get_bug_url(settings, bug, 1234)
        assert result is None


class TestGetBugSubject(object):

    def test_get_correct_subject(self):
        bug = FakeBug()
        bug.summary = 'some issue subject'
        result = get_bug_subject(bug, 1234)
        assert result == 'some issue subject'

    def test_get_fallback_subject(self):
        bug = FakeBug()
        bug.__getattr__ = lambda: (_ for _ in ()).throw(BugzillaError('boom'))
        result = get_bug_subject(bug, 1234)
        assert result == 'unable to read subject'
