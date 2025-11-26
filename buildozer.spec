[app]
title = 智能照明
package.name = lightctrl
package.domain = com.smartlight
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
# 先只跑通最纯净的 Kivy，验证环境是否成功
requirements = python3,kivy==2.2.1

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
