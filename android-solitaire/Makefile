.PHONY: all app/build/outputs/apk/debug/app-debug.apk install

all: app/build/outputs/apk/debug/app-debug.apk

install: app/build/outputs/apk/debug/app-debug.apk
	adb -d install $<

app/build/outputs/apk/debug/app-debug.apk:
	./gradlew assembleDebug
