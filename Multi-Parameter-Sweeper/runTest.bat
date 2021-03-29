SET NETSIM_PATH="C:\\Users\\TETCOS\\Documents\\NetSim_12.2.26_64_pro_default\\bin\\bin_x64"
SET NETSIM_AUTO=1
IF NOT EXIST IOPath mkdir IOPath
IF NOT EXIST Data mkdir Data
Del /Q Data\*.*
Del /Q IOPath\*.*

echo Y,THROUGHPUT(Mbps),>result.csv

FOR /L %%i IN (250,50,400) DO (
	echo | set /p=%%i, >> result.csv
	Del /F Configuration.netsim
	Del /F IOPath\Configuration.netsim
	Del /F IOPath\metrics.xml
	ConfigWriter %%i
	copy /Y configuration.netsim iopath\configuration.netsim
	"%NETSIM_PATH%\NetSimcore" -apppath "%NETSIM_PATH%" -iopath "IOPath" -license 5053@127.0.0.1
	copy /y iopath\metrics.xml metrics.xml
::	pause
	IF EXIST metrics.xml (MetricsReader result.csv) else (echo | set /p=crash >> result.csv)
	echo , >> result.csv
	copy /Y configuration.netsim Data\configuration_%%i.netsim
	copy /y metrics.xml Data\metrics_%%i.xml
	Del /Q Configuration.netsim
	Del /Q metrics.xml
)
	
