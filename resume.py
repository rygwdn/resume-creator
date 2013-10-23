#!/usr/bin/env python
# encoding: utf-8

import argparse, sys, os
import re

import yaml
import jinja2
import pypandoc

def parse_args():
    parser = argparse.ArgumentParser(
            description='Creates a resume from a template')
    parser.add_argument('data', metavar='DATA', type=argparse.FileType("r"), help='The data (YAML) file')
    parser.add_argument('template', metavar='TEMPLATE', type=str, help='The template file')
    parser.add_argument('output', metavar='OUT', type=argparse.FileType("w"), help='The output file')

    parser.add_argument('--tex', action='store_true', default=False, help='use tex-style jinja tags')

    parser.add_argument('--refs', '--references', dest='refs',
            action='store_true', default=False,
            help='include references in output')
    parser.add_argument('--norefs', '--noreferences', dest='refs',
            action='store_false', help='don\'t include references in output')

    parser.add_argument('--supervs', '--supervisors', dest='supervs',
            action='store_true', default=True,
            help='include supervisors in output')
    parser.add_argument('--nosupervs', '--nosupervisors', dest='supervs',
            action='store_false', help='don\'t include supervisors in output')

    parser.add_argument('--pers', '--personal', dest='pers',
            action='store_true', default=True,
            help='include personal data in output')
    parser.add_argument('--nopers', '--nopersonal', dest='pers',
            action='store_false', help='don\'t include personal data in output')

    parser.add_argument('--all', dest='all',
            action='store_true', default=False,
            help='include all of the above')
    parser.add_argument('--none', dest='none',
            action='store_true', default=False,
            help="don't include any of the above")

    return parser.parse_args()

def to_format(ctx, value, to_format, from_format=None, extra_args=None):
    extra_args = extra_args or tuple()
    if not from_format and "format" in ctx:
        from_format = ctx["format"]
    elif not from_format:
        from_format = "md"
    init = from_format + "_init"
    #print "in:", [value, to_format, from_format, ("--smart",) + extra_args]
    if init in ctx:
        value = ctx[init] + "\n\n" + unicode(value)
    #print "out:",
    #sys.stdout.write(unicode(pypandoc.convert(value, to_format, format=from_format, extra_args=("--smart",) + extra_args).strip()).encode('utf8'))
    #print
    #print
    return pypandoc.convert(value, to_format, format=from_format, extra_args=("--smart",) + extra_args).strip()

@jinja2.contextfilter
def any2tex(ctx, value):
    return to_format(ctx, value, "tex")

def caser(m):
    out = ":sc:{{"
    level = 0
    for chr in m.group(1):
        if chr == "{" and level >= 0:
            level += 1
        if chr == "}" and level >= 0:
            level -= 1
            if level < 0:
                out += ">>>>"
                continue
        out += chr
    if level >= 0:
        out += "}}:sc:"
    return out

sc_pat = re.compile(r"\\textsc\{(.*)\}")

@jinja2.contextfilter
def any2rst(ctx, value):
    # HACK HACK HACK HACK
    value = unicode(value)
    v = value[:]
    while sc_pat.search(value):
        value = sc_pat.sub(caser, value)
    out = to_format(ctx, value, "rst", extra_args=("--parse-raw","--filter=./delink.py"))
    out = out.replace(":sc:{{", ":sc:`").replace("}}:sc:", "`")
    return out

@jinja2.contextfilter
def cmToTbl(ctx, value):
    value = float(value)
    return int(value * (12.0 / 2.54))

def create_env(tex):
    # change the default delimiters used by Jinja
    # (prevent JinJa from interferring with LaTeX macros)
    tex_args = {}
    if tex:
        tex_args = {
                "block_start_string": '<@',
                "block_end_string": '@>',
                "variable_start_string": '<<',
                "variable_end_string": '>>',
                "comment_start_string": '<#',
                "comment_end_string": '#>',
                }
    environment = jinja2.Environment(
            autoescape = False,
            auto_reload = False,
            trim_blocks = True,
            lstrip_blocks = True,
            loader = jinja2.FileSystemLoader(os.path.abspath('.')), **tex_args)

    environment.filters["tex"] = any2tex
    environment.filters["rst"] = any2rst
    environment.filters["cmToTbl"] = cmToTbl

    return environment

def get_input(data, args):
    input = yaml.load(data.read())

    if args.none or not args.refs:
        if "references" in input:
            del input["references"]
    if args.none or not args.supervs:
        for item in input["workexp"]:
            if "superv" in item:
                del item["superv"]
    input["show_personal"] = not args.none and args.pers

    return input

def main():
    # Hack to default to utf8
    reload(sys)
    sys.setdefaultencoding('UTF-8')

    args = parse_args()
    input = get_input(args.data, args)
    environment = create_env(args.tex)
    template = environment.get_template(args.template)
    args.output.write(unicode(template.render(input)).encode('utf8'))


if __name__ == '__main__':
    main()
