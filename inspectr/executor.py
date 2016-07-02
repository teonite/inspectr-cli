import subprocess
import re


def clean(console_output):
    """Removes ANSI escape sequences from given console ouput"""
    ansi_escape = re.compile(r'\x1b[^m]*m')
    return ansi_escape.sub('', console_output)


def decode(binary_strings):
    result = []
    for bs in binary_strings:
        if isinstance(bs, str):  # sometimes we get regular strings here
            result.append(bs)
            continue
        result.append(clean(bs.decode('utf-8')))

    return result


def execute(command):
    """Executes given command with subprocess.Popen and returns it's stdout and stderr decoded"""
    if command is None:
        # some parsers depend only on previous commands output
        # and don't need to execute any command themselves
        return '', ''

    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = decode(process.communicate())
    return out, err
