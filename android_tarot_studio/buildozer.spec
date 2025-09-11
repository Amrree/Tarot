[app]

# (str) Title of your application
title = Tarot Studio

# (str) Package name
package.name = tarotstudio

# (str) Package domain (needed for android/ios packaging)
package.domain = com.tarotstudio

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd,requests,urllib3,certifi,charset-normalizer,idna

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Preset of the Android manifest, should be fullscreen, immersivesticky or
# normal
android.manifest_placeholders = android:theme="@android:style/Theme.NoTitleBar"

# (list) Android application meta-data to set (key=value format)
android.meta_data = android:theme="@android:style/Theme.NoTitleBar"

# (list) Android library project to add (will be added in the
# project.properties automatically.)
android.library_references = 

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
android.uses_library = 

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules = 

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the manifestPlaceholders property.
# This property takes a map of key-value pairs. (via a string)
# android.manifest_placeholders = 

# (bool) Skip byte compile for .py files
# android.no_bytecode_python = False

# (str) The format used to package the app for release mode (aab or apk).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aab).
# android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, if any (default: upstream)
# p4a.fork = upstream

# (str) python-for-android branch to use, if any (default: master)
# p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes = 

# (str) Filename to the hook for p4a
# p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
# p4a.port = 

# Control passing the --use-setup-py flag to p4a
# p4a.use_setup_py = False

# Control passing the --private flag to p4a
# p4a.private = 

# (str) Extra command line arguments to pass when invoking pythonforandroid.toolchain
# p4a.extra_args = 

# (str) Extra command line arguments to pass when invoking pythonforandroid.toolchain for debug builds
# p4a.extra_args_debug = 

# (str) Extra command line arguments to pass when invoking pythonforandroid.toolchain for release builds
# p4a.extra_args_release = 

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_url = https://github.com/kivy/kivy-ios
# Alternatively, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
# ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
# ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
# ios.ios_deploy_branch = 1.7.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: security find-identity -v -p codesigning
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
# ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s

# (str) The development team to use for signing the release version
# ios.codesign.development_team.release = <hexstring>

# (str) URL pointing to .ipa file to be installed
# This option should be defined along with `ios.codesign.debug` or `ios.codesign.release` to be useful
# ios.manifest.app_url = 

# (str) URL pointing to an icon file to use for the app
# This option should be defined along with `ios.codesign.debug` or `ios.codesign.release` to be useful
# ios.manifest.icon_url = 

# (str) URL pointing to a plist file to use for the app
# This option should be defined along with `ios.codesign.debug` or `ios.codesign.release` to be useful
# ios.manifest.plist_url = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's see [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,images/audio/*.wav
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#images/audio/*.wav
#
#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug