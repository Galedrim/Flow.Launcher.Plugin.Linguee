# Flow.Launcher.Plugin.Linguee

![image](https://github.com/user-attachments/assets/c410cd72-4f34-40e0-b83a-ecf613bc8971)

## Features

* Autodetect languages with language detect API (requires an API key - you can obtain one free by signing up at https://detectlanguage.com/ and following the instructions on the home page)
* Translate text with Linguee API

## Requirements

To use Python plugins within Flow-Launcher, you'll need Python 3.11 or later installed on your system. You also may need to select your Python installation directory in the Flow Launcher settings. As of v1.8, Flow Launcher should take care of the installation of Python for you if it is not on your system.

## Installing

The Plugin has been officially added to the supported list of plugins.
Run the command  ```pm install linguee``` to install it.

You can also manually add it.

## Manual

Add the plugins folder to %APPDATA%\Roaming\FlowLauncher\Plugins\ and run the Flow command ```restart Flow Launcher```.

## Python Package Requirements

This plugin automatically packs the required packages during release so for regular usage in Flow, no additional actions are needed.

If you would like to manually install the packages:

This plugin depends on the Python flow-launcher package.

Without this package installed in your Python environment, the plugin won't work!

The easiest way to install it is to open a CLI like Powershell, navigate into the plugins folder and run the following command:

``` pip install -r requirements.txt -t ./lib ```

## Usage

Type ```lg``` to start searching in Linguee.
