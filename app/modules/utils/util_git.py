#!/usr/bin/env python
# coding: utf-8
import os.path
import re
import subprocess


def git_info():
    """
    Get git info
    """
    p = subprocess.Popen(["git", "log", '-1', '--date=iso'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = str(out, encoding='UTF-8')
    rows = [r.strip() for r in out.split('\n')]
    rows = [r for r in rows if r]
    return rows


def get_git_info(output_path='data/output/git_info.txt', log=None):
    if os.path.isdir('.git'):
        lines = git_info()
        text = "\n".join(lines)

        if log:
            log(f'updating {output_path}...')

        with open(output_path, 'w') as f:
            f.write(text)

        return lines
    else:
        if os.path.isfile(output_path):
            with open(output_path, 'r') as f:
                text = f.read()

            return text.split('\n')
        else:
            return []


if __name__ == '__main__':
    get_git_info(log=print)
    pass
