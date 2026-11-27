.PHONY: run apk install install32

run:
	uv run flet run
apk:
	uv run flet build apk
install:
	adb install ./build/apk/lumbre-arm64-v8a.apk
install32:
	adb install ./build/apk/lumbre-armeabi-v7a.apk
