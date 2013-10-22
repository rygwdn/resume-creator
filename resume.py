#!/usr/bin/env python
# encoding: utf-8

import argparse, sys, os

import yaml
import jinja2
import pypandoc

def parse_args():
    parser = argparse.ArgumentParser(
            description='Creates a resume from a template')
    parser.add_argument('data', metavar='DATA', type=argparse.FileType("r"), help='The data (YAML) file')
    parser.add_argument('template', metavar='TEMPLATE', type=str, help='The template file')
    parser.add_argument('output', metavar='OUT', type=argparse.FileType("w"), help='The output file')

    #parser.add_argument('-t', '--type', dest='type',  metavar='TYPE',
    #        help='The type of output', choices=['htm','odt'], default='print')

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

def to_tex(ctx, value, format=None):
    if not format and "format" in ctx:
        format = ctx["format"]
    elif not format:
        format = "md"
    init = format + "_init"
    if init in ctx:
        value = ctx[init] + "\n\n" + value
    return pypandoc.convert(value, "tex", format=format, extra_args=("--smart",)).strip()

@jinja2.contextfilter
def any2tex(ctx, value):
    return to_tex(ctx, value)

@jinja2.contextfilter
def md2tex(ctx, md):
    return to_tex(ctx, md, format="md")

@jinja2.contextfilter
def rst2tex(ctx, rst):
    return to_tex(ctx, md, format="rst")

def create_env():
    # change the default delimiters used by Jinja
    # (prevent JinJa from interferring with LaTeX macros)
    environment = jinja2.Environment(
            block_start_string = '<@',
            block_end_string = '@>',
            variable_start_string = '<<',
            variable_end_string = '>>',
            comment_start_string = '<#',
            comment_end_string = '#>',
            autoescape = False,
            auto_reload = False,
            trim_blocks = True,
            lstrip_blocks = True,
            loader = jinja2.FileSystemLoader(os.path.abspath('.')))

    environment.filters["md"] = md2tex
    environment.filters["rst"] = rst2tex
    environment.filters["tex"] = any2tex

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
    args = parse_args()
    input = get_input(args.data, args)
    environment = create_env()
    template = environment.get_template(args.template)
    args.output.write(template.render(input))


if __name__ == '__main__':
    main()
