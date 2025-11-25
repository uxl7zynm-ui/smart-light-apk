[app]
title = 智能照明
package.name = lightctrl
package.domain = com.smartlight
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,kivy==2.2.1,BAC0,ifaddr,netifaces,requests,certifi,urllib3,idna,chardet
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, CHANGE_WIFI_MULTICAST_STATE
android.api = 33
android.minapi = 24
android.ndk_api = 25
android.archs = arm64-v8a
p4a.branch = develop
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
