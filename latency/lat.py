import shlex
from subprocess import Popen, PIPE, STDOUT


def get_simple_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a simple external command and get its output.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]


def get_ping_time(host):
    cmd = "fping {host} -C 3 -q".format(host=host)
    res = [float(x) for x in get_simple_cmd_output(cmd).strip().split(':')[-1].split() if x != '-']
    if len(res) > 0:
        return sum(res) / len(res)
    else:
        return 999999