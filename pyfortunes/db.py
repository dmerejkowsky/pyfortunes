import os
import re
import subprocess
import sys

import pyfortunes.config


class FortuneDB():
    def __init__(self):
        self.base_dir = None
        self.fortunes = None
        self.parse_config()

    def commit(self, category):
        fortune_file = os.path.join(self.base_dir, category)
        rc = subprocess.call(["vim", fortune_file])
        if rc != 0:
            sys.exit(rc)
        self._run_git("add", fortune_file)
        self._run_git("commit", "--message", "update %s" % category)

    def sync(self):
        # Make sure we are always up-to-date, even in case of push-f
        rc, out = self._run_git("status", "--porcelain", abort_on_error=False)
        if rc != 0:
            print(out)
            sys.exit(rc)
        for line in out.splitlines():
            if line.startswith("M"):
                sys.exit("Your worktree is not clean")
        self._run_git("fetch")
        self._run_git("reset", "--hard", "origin/master")

    def push(self):
        cmd = ["diff", "--color=always", "--word-diff",
               "HEAD~1", "HEAD"
        ]
        rc, out = self._run_git(*cmd, abort_on_error=False)
        if rc != 0:
            print(out)
            sys.exit(1)
        sys.stdout.write(out)
        answer = input("OK to push? (Y/n)")
        if answer in ["y", "Y", ""]:
            self._run_git("push")

    def parse_config(self):
        config = pyfortunes.config.get_config()
        self.base_dir = config["text_db"]["base_dir"]

    def parse_fortunes(self):
        fortune_files = os.listdir(self.base_dir)
        fortune_files = [x for x in fortune_files if x != ".gitignore"]
        fortune_files = [os.path.join(self.base_dir, x) for x in fortune_files]
        fortune_files = [x for x in fortune_files if os.path.isfile(x)]
        fortune_files.sort()
        fortune_files = [x for x in fortune_files if not os.path.splitext(x)[1]]
        self.fortunes = dict()
        for fortune_file in fortune_files:
            category = os.path.basename(fortune_file)
            self.fortunes[category] = self._parse_fortunes_in_category(category)

    def append_and_push(self, text, *, category=None):
        self.sync()
        self.append_fortune(text, category=category)
        self.commit(category)
        self.push()

    def append_fortune(self, text, *, category=None):
        fortunes = self._parse_fortunes_in_category(category, verbose=False)
        last = len(fortunes)
        fortune_file = os.path.join(self.base_dir, category)
        with open(fortune_file, "a") as fp:
            fp.write("%{}\n".format(last + 1))
            fp.write(text)

    def _parse_fortunes_in_category(self, category, verbose=True):
        if verbose:
            print("Parsing", category)
        fortune_file = os.path.join(self.base_dir, category)
        res = list()
        cur_text = ""
        cur_index = 0
        cur_fortune = None
        with open(fortune_file, "r") as fp:
            lines = fp.readlines()
        for line in lines:
            match = re.match("^%(\d+)$", line)
            if match:
                index = match.groups()[0]
                cur_index += 1
                if int(index) != cur_index:
                    print(line)
                    sys.exit("Expecting %i, got %s" % (cur_index, index))
                if cur_text:
                    res.append(cur_text)
                cur_text = ""
            else:
                cur_text += line
        # last line: append the last fortune
        if cur_text:
            res.append(cur_text)
        return res

    def _run_git(self, *args, abort_on_error=True):
        cmd = ("git", ) + args
        env = os.environ.copy()
        for key in list(env.keys()):
            if "GIT" in key:
                del env[key]
        if abort_on_error:
            rc = subprocess.call(cmd, cwd=self.base_dir, env=env)
            if rc != 0:
                sys.exit(rc)
        else:
            process = subprocess.Popen(cmd, cwd=self.base_dir, env=env,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            out, _ = process.communicate()
            return process.returncode, out.decode("utf-8")
