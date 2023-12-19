#!/usr/bin/python -tt
# Project: cli_input_standardization
# Filename: gen_cisco_nexus_vpc_inf_configlet.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "12/19/23"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import yaml
import pprint
import jinja2
import datetime
import re
import os


def open_yaml(yfil = "cisco_nexus_vpc_intf_design_payload.yml"):
    """
    Open a YAML file and return contents (or empty dictioinary)
    :param yfil:
    :return: yfil_data which should have the file contents
    """

    try:
        with open(yfil, 'r') as file:
            yfil_data = yaml.safe_load(file)
    except:
        yfil_data = dict()
    return yfil_data


def write_rendered_to_file(full_file_path=os.getcwd(), content="", filename='configlet.txt', mode="w"):
    """
    Take Jinja2 rendered output and write to a file
    :param full_file_path: Directory
    :param content: rendered content
    :param filename: filename which defaults to configlet.txt
    :param mode: file open mode defaults to write (w)
    :return: wrote_file Boolean True if there was content and a file was created and False if no content
    """

    output_filename = os.path.join(full_file_path, filename)
    if content:
        with open(output_filename, mode) as outfile:
            content_with_lines = content.splitlines()
            for line in content_with_lines:
                outfile.write(line + "\n")
        wrote_file = True
    else:
        wrote_file = False
    return wrote_file


def render_j2template_fp(cfg, j2_template):
    """
    Render the Jinja2 Template with the values
    :param cfg: dictionary of configuration values for template
    :param j2_template:  Jinja2 template
    :return: rendered content
    """

    with open(j2_template) as file_:
        template = jinja2.Template(file_.read())

    rendered = template.render(cfg=cfg)

    return rendered


def get_int_num(intf, debug=False):
    """
    Function that parses the interface and returns the last interface number
    For example: Gi1/0/17
    Returns string "17"
    """
    int_only = re.sub(r"^\s*\D{2,3}", "", intf)
    _ = intf.split("/")
    if debug:
        print(int_only)
        print(f"\n\n{_}")
        print(type(_[-1]))

    return _[-1]


def main():

    # Set Creation Timestamp
    file_timestamp = datetime.datetime.now().strftime(
        "%d-%m-%Y  %H%M%S"
    )

    # Load the YAML Design Payload file which contains the required details
    cfg_payload = open_yaml()

    # Pretty Print configuration payload loaded
    pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint((cfg_payload))

    # Add the creation timestamp to the payload file
    cfg_payload.update({"timestamp": file_timestamp})

    # For each item in design_payload
    for item, item_dict in cfg_payload['design_payload'].items():

        start_intf = item_dict['intf_start']
        num_intf = item_dict['total_intfs_per_dev']

        # Calculate PO/vPC
        intf_num = int(get_int_num(start_intf))
        vpc = 1000 + intf_num
        cfg_payload['design_payload'][item].update({'vpc': vpc})

        # Derive interface
        itext = ""
        for i in range(0, num_intf):
            if not itext:
                itext = f"Ethernet{start_intf}"
            else:
                itext = f"{itext}, Ethernet1/{intf_num+i}"
        cfg_payload['design_payload'][item].update({'intf': itext})
        pp.pprint((cfg_payload['design_payload'][item]))
        print("-----")
    jtemplate = "cisco_nexus_vpc_intf_template.j2"
    output = render_j2template_fp(cfg_payload, jtemplate)
    print("\n\nOUTPUT:")
    # print(output)

    write_rendered_to_file(content=output)

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python gen_cisco_nexus_vpc_inf_configlet.py' ")

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()
    main()
