import subprocess


def test_process_command(command):
    return subprocess.check_output(command.rstrip(), shell=True, stderr=subprocess.STDOUT)
