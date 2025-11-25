[app]
title = 智能照明
package.name = lightctrl
package.domain = com.smartlight
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
# 这里的依赖非常重要，加上 openssl 保证网络请求正常
requirements = python3,kivy==2.2.1,BAC0,ifaddr,netifaces,requests,certifi,urllib3,idna,chardet,openssl

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, CHANGE_WIFI_MULTICAST_STATE

# 安卓版本配置
android.api = 33
android.minapi = 24
android.ndk_api = 25
android.archs = arm64-v8a
android.allow_backup = True

# 关键修复：使用最新的 python-for-android 分支
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
