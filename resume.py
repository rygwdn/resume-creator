#!/usr/bin/env python
# encoding: utf-8

import argparse, sys

import yaml
from Cheetah.Template import Template
from Cheetah.Filters import Filter
from docutils import core


RST_REPLACES = [
        (r"--", r"-"),
        (r"~", r" "),
        ]

LATEX_REPLACES = [
        (r"LaTeX", r"{\fb \LaTeX} \fontReset"),
        (r"\textasciitilde{}", r"~"),
        (r"-{}-", r"--"),
        ]

namespace = []

class CleanRst(Filter):
    def filter(self, val, **kw):
        out = unicode(val).strip()
        for fr, to in RST_REPLACES:
            out = out.replace(fr, to)
        return out

class StrpRst(CleanRst):
    def filter(self, val, **kw):
        out = CleanRst.filter(self, val, **kw)
        out = out.replace(r"`", "")
        out = out.replace(r":sc:", "")
        return out

class Rst2Tex(Filter):
    def filter(self, val, **kw):
        input = namespace["rst_init"].strip()
        input += "\n\n\n"
        input += unicode(val)
        out = core.publish_parts(
                source=input,
                writer_name='latex'
                )["body"]
        out = out.strip()
        for fr, to in LATEX_REPLACES:
            out = out.replace(fr, to)
        return out

def parse_args():
    parser = argparse.ArgumentParser(
            description='Creates a resume from a template')
    parser.add_argument('data', metavar='DATA', type=file,
            help='The data (YAML) file')
    parser.add_argument('template', metavar='TEMPLATE', type=file, nargs='?',
            help='The template file', default=sys.stdin)
    parser.add_argument('output', metavar='OUT', type=argparse.FileType("w"), nargs='?',
            help='The output file', default=sys.stdout)
    parser.add_argument('-t', '--type', dest='type',  metavar='TYPE',
            help='The type of output', choices=['htm','odt'], default='print')

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

def gen_namespace(ns):
    ns["rst2tex"] = Rst2Tex
    ns["clean_rst"] = CleanRst
    ns["strp_rst"] = StrpRst
    ns["outp"] = ["base"]

    ns["tex_init"] = core.publish_parts(
            ns["rst_init"].strip()
            )
    return ns

def main():
    global namespace

    args = parse_args()
    namespace = gen_namespace(yaml.load(args.data.read()))
    namespace['type'] = args.type

    if not args.none:
        if args.all or args.refs:
            namespace['outp'] += ["references", "refs"]
        if args.all or args.supervs:
            namespace['outp'] += ["supervs", "supervisors"]
        if args.all or args.pers:
            namespace['outp'] += ["pers", "personal"]

    template_def = args.template.read()

    template = Template(template_def, [namespace])

    args.output.write(str(template))
    args.output.flush()
    args.output.close()

if __name__ == '__main__':
    main()
