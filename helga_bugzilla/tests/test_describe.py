from helga_bugzilla.actions.describe import match
from helga_bugzilla.actions.describe import construct_message
from helga_bugzilla.actions.describe import send_message
import pytest
from attrdict import AttrDict


def line_matrix():
    pre_garbage = [' ', '', 'some question about ']
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
    pre_garbage = [' ', '', 'some question about ']
    pre_prefixes = ['', ' ', 'f']
    prefixes = ['bug', 'BuG', 'bz', 'rhbz', 'RHBZ']
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


multiple_ticket_lines = [
    'bugs #1 #2 #3',
    'bugs 1, 2, 3',
    'bugs 1, 2 and 3',
    'bugs 1, 2, and 3',
    'bugs 1 and 2 and 3',
    'bugs 1, and 2, and 3',
]


class TestIsTicket(object):

    @pytest.mark.parametrize('line', line_matrix())
    def test_matches(self, line):
        assert len(match(line)) > 0

    @pytest.mark.parametrize('line', fail_line_matrix())
    def test_does_not_match(self, line):
        assert match(line) == []

    @pytest.mark.parametrize('line', multiple_ticket_lines)
    def test_matches_multiple_tickets(self, line):
        assert match(line) == ['1', '2', '3']

    def test_ignore_bz2(self):
        line = 'please download the ceph.tar.bz2 file'
        assert match(line) == []

    def test_dedupe(self):
        line = 'bug 1 and bug 1'
        assert match(line) == ['1']


class FakeClient(object):
    """
    Fake Helga client (eg IRC or XMPP) that simply saves the last
    message sent.
    """
    def msg(self, channel, msg):
        self.last_message = (channel, msg)


class TestSendMessage(object):
    def test_send_message(self):
        bug = AttrDict({'summary': 'some issue subject',
                        'weburl': 'http://bz.example.com/1'})
        client = FakeClient()
        channel = '#bots'
        nick = 'ktdreyer'
        # Send the message using our fake client
        send_message([bug], ['bz#1'], client, channel, nick)
        expected = ('ktdreyer might be talking about '
                    'http://bz.example.com/1 [some issue subject]')
        assert client.last_message == (channel, expected)


class TestConstructMessage(object):

    def test_construct_message(self):
        bug = AttrDict({'summary': 'some issue subject',
                        'weburl': 'http://bz.example.com/1'})
        nick = 'ktdreyer'
        result = construct_message([bug], nick)
        expected = ('ktdreyer might be talking about '
                    'http://bz.example.com/1 [some issue subject]')
        assert result == expected

    def test_two_tickets(self):
        bugs = []
        bugs.append(AttrDict({'summary': 'some issue subject',
                              'weburl': 'http://bz.example.com/1'}))
        bugs.append(AttrDict({'summary': 'another issue subject',
                              'weburl': 'http://bz.example.com/2'}))
        nick = 'ktdreyer'
        result = construct_message(bugs, nick)
        expected = ('ktdreyer might be talking about '
                    'http://bz.example.com/1 [some issue subject] and '
                    'http://bz.example.com/2 [another issue subject]')
        assert result == expected

    def test_four_tickets(self):
        """ Verify that commas "," and "and" get put in the right places. """
        bugs = []
        bugs.append(AttrDict({'summary': 'subj 1',
                              'weburl': 'http://bz.example.com/1'}))
        bugs.append(AttrDict({'summary': 'subj 2',
                              'weburl': 'http://bz.example.com/2'}))
        bugs.append(AttrDict({'summary': 'subj 3',
                              'weburl': 'http://bz.example.com/3'}))
        bugs.append(AttrDict({'summary': 'subj 4',
                              'weburl': 'http://bz.example.com/4'}))
        nick = 'ktdreyer'
        result = construct_message(bugs, nick)
        expected = ('ktdreyer might be talking about '
                    'http://bz.example.com/1 [subj 1], '
                    'http://bz.example.com/2 [subj 2], '
                    'http://bz.example.com/3 [subj 3] and '
                    'http://bz.example.com/4 [subj 4]')
        assert result == expected
