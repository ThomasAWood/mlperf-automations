del /Q %MLC_JAVAC_PREBUILT_FILENAME%.zip

wget --no-check-certificate %MLC_JAVAC_PREBUILT_URL%%MLC_JAVAC_PREBUILT_FILENAME%.zip
IF %ERRORLEVEL% NEQ 0 EXIT %ERRORLEVEL%

unzip %MLC_JAVAC_PREBUILT_FILENAME%.zip
IF %ERRORLEVEL% NEQ 0 EXIT %ERRORLEVEL%

del /Q %MLC_JAVAC_PREBUILT_FILENAME%.zip
