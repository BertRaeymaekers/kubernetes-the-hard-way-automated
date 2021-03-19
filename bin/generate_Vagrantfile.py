#! /usr/bin/env python3

from collections import defaultdict
import os
import sys

import jinja2


OPTIONS = {
    "-f": "from",
    "--from": "from",
    "-t": "to",
    "-to": "to",
    "--numbers": "numbers",
    "-n": "numbers",
}

OPTION_TYPES = {
    "from": int,
    "to": int,
}

OPTION_DEFAULTS = ["vb", "kubdoc"]


def do_template(src, dest, template_path=None, **kwargs):
    if template_path is None:
        template_path = "../vagrant/templates/"
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    jinja_template = jinja_env.get_template(src)
    output_from_parsed_template = jinja_template.render(**kwargs)
    # print(output_from_parsed_template)
    with open(dest, "w") as fh:
        fh.write(output_from_parsed_template)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    args = defaultdict(list)
    current_arg = None
    for arg in sys.argv[1:]:
        if arg[0] == "-":
            try:
                arg_type = OPTION_TYPES.get(current_arg, str)(int(arg))
                args[current_arg].append(arg_type)
            except ValueError:
                current_arg = OPTIONS.get(arg, "")
        else:
            args[current_arg].append(OPTION_TYPES.get(current_arg, str)(arg))
            current_arg = None

    print(args)
    print("Called with arguments:")
    print("\t%s" % (", ".join(args.get(None, []))))
    for key, value in args.items():
        if key:
            print("\t%s: %s" % (key, value))
    # TODO: missing options (REQUIRED_OPTIONS)
    # TODO: unknown options

    i_from = args.get("from", [0])[0]
    i_to = args.get("to", [i_from])[0]
    numbers = ",".join(args.get("numbers", [])).split(",")
    if numbers == [""]:
        numbers = []
    single_args = args.get(None, [])
    single_args = [single_args[i] if len(single_args) > i else OPTION_DEFAULTS[i] for i in range(len(OPTION_DEFAULTS))]    
    template, internal_network_name = single_args
    machine_numbers = set(range(i_from, i_to + 1)).union(set(map(int, numbers)))
    print()
    print("Numbers:", machine_numbers)

    # Generate the Vagrantfile
    do_template(
        "Vagrantfile.%s.j2" % (template),
        "../Vagrantfile",
        machine_numbers=machine_numbers,
        internal_network_name=internal_network_name,
        internal_network_a=192,
        internal_network_b=168,
        internal_network_c=50,
        internal_network_d=1,
    )
