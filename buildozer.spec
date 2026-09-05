[app]

title = Superior Siyoma Calculator
package.name = superiorsiyoma
package.domain = org.siyomacodingprograms

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 2.0

# Pin Kivy so python-for-android builds against a known-good
# recipe instead of whatever "latest" happens to be that week.
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Uncomment once you add a 512x512 icon.png to this folder.
# icon.filename = %(source.dir)s/icon.png

# --- Android specifics ---
android.permissions =

# Covers essentially all real phones in use today, old and new.
android.archs = arm64-v8a, armeabi-v7a

android.minapi = 21
android.api = 34
android.ndk = 25b

android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 1
