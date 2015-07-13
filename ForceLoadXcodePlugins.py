#!/usr/bin/env python

import sys
import glob, os
import argparse
import syslog

nr_of_updated_plugins = 0

try:
    import biplist
except ImportError as e:
    print("'biplist' module is not installed. Please run 'sudo easy_install biplist' to install it.")
    syslog.syslog(syslog.LOG_ERR, str(e))
    sys.exit(1)

def main(argv):

    ARG_PATH_XCODE_PATH = "xcode_path"
    ARG_PATH_PLUGIN_PATH = "plugin_path"
    ARG_PATH_MARK = "mark"

    parser=argparse.ArgumentParser(
        description=argv[0] + " can be used to mark the 3rd party Xcode plugins as compatible with the Xcode.app that you provide a path to or the one that's automatically discovered.",
        epilog="Happy Xcoding!")
    parser.add_argument("-x", "--xcode-path", dest=ARG_PATH_XCODE_PATH, default="/Applications/Xcode.app", help="path to the Xcode.app")
    parser.add_argument("-p", "--plugin-path", dest=ARG_PATH_PLUGIN_PATH, default="", help="mark only the plugin found at this path")
    parser.add_argument("-a", "--all-plugins", dest=ARG_PATH_PLUGIN_PATH, action="store_const", const="", help="mark all the 3rd party plugins found")
    parser.add_argument("-m", "--mark", dest=ARG_PATH_MARK, action="store_true", default=True, help="make the plugin(s) compatible")
    parser.add_argument("-u", "--unmark", dest=ARG_PATH_MARK, action="store_false", help="make the plugin(s) incompatible")
    args=vars(parser.parse_args())

    xcode_path = args[ARG_PATH_XCODE_PATH]
    plugin_path = args[ARG_PATH_PLUGIN_PATH]
    mark = args[ARG_PATH_MARK]

    uuid = getuuid(xcode_path)

    print("Found Xcode UUID '" + uuid + "'.")
    print("")

    if plugin_path:
        updated = mark_uuid(plugin_path, uuid, mark)

    else:
        try:
            plugins_base_path = os.path.expanduser("~/Library/Application Support/Developer/Shared/Xcode/Plug-ins/")
            os.chdir(plugins_base_path)
        except Exception as e:
            print("Could not find plugins directory '" + plugins_base_path + "'.")
            syslog.syslog(syslog.LOG_ERR, str(e))
            sys.exit(2)

        for file in glob.glob("*.xcplugin"):
            mark_uuid(os.path.abspath(plugins_base_path) + os.path.sep + file, uuid, mark)

        if nr_of_updated_plugins == 0:
            if mark:
                print("All plugins are already marked.")
            else:
                print("All plugins are already unmarked.")

def getuuid(xcode_path):

    info_file_path = os.path.abspath(xcode_path) + os.path.sep + "Contents/Info.plist"

    try:
        pl = biplist.readPlist(info_file_path)
    except Exception as e:
        print("Could not open file '" + info_file_path + "'.")
        syslog.syslog(syslog.LOG_ERR, str(e))
        sys.exit(3)

    key = "DVTPlugInCompatibilityUUID"
    if key in pl.keys():
        return pl[key]
    else:
        print("Could not find the UUID in '" + info_file_path + "'.")
        sys.exit(4)

def mark_uuid(plugin_abspath, uuid, mark = True):

    global nr_of_updated_plugins
    info_file_path = os.path.abspath(plugin_abspath) + os.path.sep + "Contents/Info.plist"

    try:
        pl = biplist.readPlist(info_file_path)

        key = "DVTPlugInCompatibilityUUIDs"
        if not key in pl.keys():
            print("Could not find the UUIDs in '" + info_file_path + "'.")
            return False

        uuids = pl[key]
        updated = False

        if mark:
            if uuid not in uuids:
                uuids.append(uuid)
                updated = True
        else:
            if uuid in uuids:
                uuids.remove(uuid)
                updated = True

        try:
            biplist.writePlist(pl, info_file_path)

            if updated:
                if mark:
                    print("Marked '" + os.path.basename(plugin_abspath) + "'.")
                else:
                    print("Unmarked '" + os.path.basename(plugin_abspath) + "'.")
                nr_of_updated_plugins += 1

            return updated

        except Exception as e:
            print("Could not update the file '" + info_file_path + "'.")
            syslog.syslog(syslog.LOG_ERR, str(e))
            return False

    except Exception as e:
        print("Could not open file '" + info_file_path + "'.")
        syslog.syslog(syslog.LOG_ERR, str(e))

if __name__ == "__main__":
    main(sys.argv)
