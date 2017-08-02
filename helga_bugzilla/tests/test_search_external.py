from helga_bugzilla.actions.search_external import match
from helga_bugzilla.actions.search_external import construct_message
from helga_bugzilla.actions.search_external import send_message
import pytest
from attrdict import AttrDict


def line_matrix():
    # "what bz is tracker.ceph.com/issues/19055 ?"
    # "what's the bz for tracker.ceph.com/issues/19055 ?"
    phrase = '{question} {bug} {action} {external}'
    questions = [
        "which",
        "what",
        "whats the",
        "what's the",
        "what is the",
        "wheres the",
        "where's the",
        "where is the",
    ]
    bugs = ['bz', 'bug', 'rhbz', 'bugzilla']
    actions = [
        'is',
        'matches',
        'tracks',
        'corresponds to',
        'relates to',
        'for',
        'that is',
        'that matches',
        'that tracks',
        'that corresponds to',
    ]
    externals = ['tracker.ceph.com/issues/19055',
                 'http://tracker.ceph.com/issues/19055']
    lines = []
    for question in questions:
        for bug in bugs:
            for action in actions:
                for external in externals:
                        line = phrase.format(question=question, bug=bug,
                                             action=action, external=external)
                        lines.append(line)
    return lines


class TestIsMatch(object):

    @pytest.mark.parametrize('line', line_matrix())
    def test_matches(self, line):
        result = match(line)
        assert len(result) > 0
        assert 'tracker.ceph.com/issues/19055' in result[0]


class TestConstructMessage(object):

    def test_construct_message(self):
        ticket = 'tracker.ceph.com/issues/19055'
        bug = AttrDict({'summary': 'some issue subject',
                        'weburl': 'http://bz.example.com/1'})
        nick = 'ktdreyer'
        result = construct_message(ticket, [bug], nick)
        expected = ('ktdreyer, tracker.ceph.com/issues/19055 is '
                    'http://bz.example.com/1 [some issue subject]')
        assert result == expected


class FakeClient(object):
    """
    Fake Helga client (eg IRC or XMPP) that simply saves the last
    message sent.
    """
    def msg(self, channel, msg):
        self.last_message = (channel, msg)


class TestSendMessage(object):

    def test_no_send_message(self):
        client = FakeClient()
        channel = '#bots'
        send_message(False, [], client, channel, 'ktdreyer')
        assert getattr(client, 'last_message', None) is None

    def test_send_message(self):
        ticket = 'tracker.ceph.com/issues/19055'
        bugs = [AttrDict({'summary': 'some issue subject',
                          'weburl': 'http://bz.example.com/1'})]
        ticket_and_bugs = (ticket, bugs)
        links = [ticket]
        client = FakeClient()
        channel = '#bots'
        # Send the message using our fake client
        send_message(ticket_and_bugs, links, client, channel, 'ktdreyer')
        expected = ('ktdreyer, tracker.ceph.com/issues/19055 is '
                    'http://bz.example.com/1 [some issue subject]')
        assert client.last_message == (channel, expected)

# I've commented out this test because it's unique to my workstation. I used it
# to run through my entire IRC log history and spot-check that
# search_external.py was only going to trigger on appropriate phrases. I don't
# want our bot to fire on spurious comments about "what BZ ...". So far so
# good.
#
#
# def log_files():
#     import os
#     result = []
#     logdir = '/home/kdreyer/.purple/logs'
#     for root, dirs, files in os.walk(logdir):
#         for logfile in files:
#             if logfile.endswith('.txt'):
#                 if 'ktdreyer@localhost' in root:
#                     # Lots of false-positives here as I test things out
#                     continue
#                 result.append(os.path.join(root, logfile))
#     return result
#
#
# class TestLogs(object):
#     @pytest.mark.parametrize('filename', log_files())
#     def test_log(self, filename):
#         result = []
#         with open(filename, 'r') as logh:
#             for line in logh:
#                 result = match(line)
#                 assert len(result) == 0, line
