import os
import shlex
import subprocess


TOP = os.path.join(os.path.dirname(__file__), "..")


class Command(object):
    COMMAND_MAP = {
        "bdgt": {
            "bin": os.path.normpath("{0}/bin/bdgt".format(TOP)),
            "args": ['-d', 'sqlite:///test.db'],
        }
    }

    @classmethod
    def run(cls, cmd):
        cmd_split = shlex.split(cmd)
        given_cmd = cmd_split[0]
        if given_cmd in cls.COMMAND_MAP:
            for arg in reversed(cls.COMMAND_MAP[given_cmd]["args"]):
                cmd_split.insert(1, arg)
            cmd_split[0] = cls.COMMAND_MAP[given_cmd]["bin"]
        return subprocess.check_output(cmd_split)


def before_scenario(context, scenario):
    if os.path.exists('test.db'):
        assert False


def after_scenario(context, scenario):
    if os.path.exists('test.db'):
        os.remove('test.db')


def before_all(context):
    context.cmd_line = Command
