[app]

# اسم التطبيق
title = الأجندة القضائية

# اسم الحزمة (package name)
package.name = agendalawyer

# نطاق الحزمة
package.domain = org.agenda

# إصدار التطبيق
version = 1.0.0

# الملف الرئيسي
source.dir = .

# امتدادات الملفات المطلوبة
source.include_exts = py,png,jpg,kv,atlas,ttf

# المتطلبات (المكتبات)
requirements = python3,kivy,kivymd,requests,arabic-reshaper,python-bidi

# اتجاه الشاشة (عمودي)
orientation = portrait

# حجم الأيقونة (اختياري)
icon.filename = icon.png

# الاسم الكامل للتطبيق
fullscreen = 0

# دعم الأندرويد
android.api = 33
android.minapi = 21
android.gradle_dependencies = 
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.ndk = 25b
android.sdk = 33

# تشغيل التطبيق تلقائياً بعد التثبيت
android.auto_launch = False

# دعم الشاشات الكبيرة
android.adaptive.launcher = True
android.adaptive.icon.foreground = icon.png
android.adaptive.icon.background = #0F172A