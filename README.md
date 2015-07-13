# ForceLoadXcodePlugins
---

## Description

`ForceLoadXcodePlugins.py` is a script that lets you to mark the 3rd party Xcode plugins as
compatible with the Xcode.app that you provide a path to or the one that's
automatically discovered.

## Usage

```
ForceLoadXcodePlugins.py [-h] [-x XCODE_PATH] [-p PLUGIN_PATH] [-a] [-m] [-u]

optional arguments:
  -h, --help                                show this help message and exit
  -x XCODE_PATH, --xcode-path XCODE_PATH    path to the Xcode.app
  -p PLUGIN_PATH, --plugin-path PLUGIN_PATH mark only the plugin found at this path
  -a, --all-plugins                         mark all the 3rd party plugins found
  -m, --mark                                make the plugin(s) compatible
  -u, --unmark                              make the plugin(s) incompatible
```

## Examples

Mark all the 3rd party plugins as compatible with the current version of Xcode.
```
python ForceLoadXcodePlugins.py
```

Mark all the 3rd party plugins as compatible with a beta version of Xcode.
```
python ForceLoadXcodePlugins.py --xcode-path=/Applications/Xcode-beta.app/
```

Mark the `Alcatraz` plugin as compatible with the current version of Xcode.
```
python ForceLoadXcodePlugins.py --plugin-path=/Users/arturgrigor/Library/Application\ Support/Developer/Shared/Xcode/Plug-ins/Alcatraz.xcplugin
```

## Requirements

This script requires `Python` >= 2.7 and the `biplist` Python module. The `biplist` can be easily installed by running `sudo easy_install biplist`.
