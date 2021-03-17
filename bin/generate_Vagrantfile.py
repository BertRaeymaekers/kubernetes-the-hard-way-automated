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
    "--controllers": "controllers",
    "-c": "controllers",
}

OPTION_TYPES = {
    "from": int,
    "to": int,
}


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
                args[current_arg].append(OPTION_TYPES.get(current_arg, str)(int(arg)))
            except ValueError:
                current_arg = OPTIONS.get(arg, "")
        else:
            args[current_arg].append(OPTION_TYPES.get(current_arg, str)(arg))

    print("Called with arguments:")
    print("\t%s" % (", ".join(args.get(None, []))))
    for key, value in args.items():
        if key:
            print("\t%s: %s" % (key, value))
    # TODO: missing options (REQUIRED_OPTIONS)
    # TODO: unknown options

    i_from = args.get("from", [0])[0]
    i_to = args.get("to", [i_from])[0]
    template = args.get(None, ["vb"])[0]
    count = set(range(i_from, i_to + 1))
    controllers = set(map(int, ",".join(args.get("controllers", [])).split(",")))
    workers = count - controllers
    print()
    print("Controllers:", controllers)
    print("Workers:    ", workers)

    # Generate the Vagrantfile
    do_template(
        "Vagrantfile.%s.j2" % (template),
        "../Vagrantfile",
        count=count,
        controllers=controllers,
        workers=workers,
    )
