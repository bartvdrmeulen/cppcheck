# Test if --bug-hunting works using cve tests

import glob
import os
import re
import shutil
import sys
import subprocess

if sys.argv[0] in ('test/bug-hunting/cve.py', './test/bug-hunting/cve.py'):
    CPPCHECK_PATH = './cppcheck'
    TEST_SUITE = 'test/bug-hunting/cve'
else:
    CPPCHECK_PATH = '../../cppcheck'
    TEST_SUITE = 'cve'

def test(test_folder):
    print(test_folder)

    cmd_file = os.path.join(test_folder, 'cmd.txt')
    expected_file = os.path.join(test_folder, 'expected.txt')

    cmd = [CPPCHECK_PATH,
           '-D__GNUC__',
           '--bug-hunting',
           '--inconclusive',
           '--platform=unix64',
           '--template={file}:{line}:{id}',
           '-rp=' + test_folder,
           test_folder]

    if os.path.isfile(cmd_file):
        for line in open(cmd_file, 'rt'):
            if len(line) > 1:
                cmd.append(line.strip())

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comm = p.communicate()
    stdout = comm[0].decode(encoding='utf-8', errors='ignore')
    stderr = comm[1].decode(encoding='utf-8', errors='ignore')

    with open(expected_file, 'rt') as f:
        for expected in f.readlines():
            if expected.strip() not in stderr.split('\n'):
                print('FAILED. Expected result not found: ' + expected)
                print('Command:')
                print(' '.join(cmd))
                print('Output:')
                print(stderr)
                sys.exit(1)

if len(sys.argv) > 1:
    test(sys.argv[1])
    sys.exit(0)

for test_folder in sorted(glob.glob(TEST_SUITE + '/CVE*')):
    test(test_folder)

