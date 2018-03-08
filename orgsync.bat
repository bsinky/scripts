@ECHO OFF

rem Script to sync org-mode files stored in the home directory to cloude storage.
rem 
rem Windows version

REM https://stackoverflow.com/a/1445724/4276832
SET HOUR=%time:~0,2%
SET dtStamp9=%date:~-4%%date:~4,2%%date:~7,2%_0%time:~1,1%%time:~3,2%%time:~6,2% 
SET dtStamp24=%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%

if "%HOUR:~0,1%" == " " (SET dtStamp=%dtStamp9%) else (SET dtStamp=%dtStamp24%)

SET logdir=%USERPROFILE%\orglogs\
SET logfile=%logdir%%dtStamp%.log

IF NOT EXIST %logdir% mkdir %logdir%

REM Create logfile is it does not exist - https://stackoverflow.com/a/211045/4276832
IF NOT EXIST %logfile% copy /y NUL %logfile% >NUL

rclone copy google:org %USERPROFILE%\org -v -u --log-file %USERPROFILE%\orglogs\%dtStamp%.log
rclone sync %USERPROFILE%\org google:org -v -u --log-file %USERPROFILE%\orglogs\%dtStamp%.log