#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import *
import platform
import os

def pipe_through_prog(argv, text):
    p1 = Popen(argv, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    [result, err] = p1.communicate(input=text.encode('utf-8'))
    return [p1.returncode, result.decode('utf-8'), err]

class Prog:
    def __init__(self, cmdline="md2latex", default_options=["-f"]):
        self.cmdline = cmdline.split()
        if len(self.cmdline) <= 1:
            # cmdline provided no command line options. Use default ones.
            if isinstance(default_options, str):
                self.cmdline += default_options.split()
            else:
                self.cmdline += default_options
        self.to_latex = lambda x: pipe_through_prog(self.cmdline, x)

def run_test (prog,test_name):
     print("running ", test_name)
     with open('./'+test_name+'.md', 'r') as file:
        input = file.read()
        isExist = os.path.exists(test_name)
        if not isExist:
            os.mkdir(test_name)
        os.chdir(test_name)
        output=prog.to_latex(input)
        print(output)
        latex_file_name= test_name+'.tex'
        output_file = open(latex_file_name, 'w')
        output_file.write(output[1])
        output_file.close()
        status=run(["lualatex",latex_file_name ])
        print(status)
        os.chdir("..")


if __name__ == "__main__":
    md2latex = Prog()
    run_test(md2latex,"test_bold")
    run_test(md2latex,"test_unordered_list")
    run_test(md2latex,"test_ordered_list")
    run_test(md2latex,"test_italic")
    run_test(md2latex,"test_italic2")
    run_test(md2latex,"test_formula")
   