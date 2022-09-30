.PHONY: all app/build/outputs/apk/debug/app-debug.apk app/build/outputs/apk/release/app-release.apk clean debug install

all: debug

debug: app/build/outputs/apk/debug/app-debug.apk
	adb -d install $<
install: app/build/outputs/apk/release/app-release.apk
	adb install $<

app/build/outputs/apk/debug/app-debug.apk:
	./gradlew assembleDebug
app/build/outputs/apk/release/app-release.apk:
	./gradlew assembleRelease

clean:
	rm -rf app/build/
