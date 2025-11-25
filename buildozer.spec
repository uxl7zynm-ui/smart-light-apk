[app]
title = 智能照明
package.name = lightctrl
package.domain = com.smartlight
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
# 增加 openssl 依赖
requirements = python3,kivy==2.2.1,BAC0,ifaddr,netifaces,requests,certifi,urllib3,idna,chardet,openssl

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, CHANGE_WIFI_MULTICAST_STATE

# 适配新版安卓
android.api = 33
android.minapi = 24
android.ndk_api = 25
android.archs = arm64-v8a

# 【关键】使用 master 分支解决兼容性
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
