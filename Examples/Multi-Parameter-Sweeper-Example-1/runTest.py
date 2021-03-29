import random
import shutil
import math
import sys
import os

#Set the path of NetSim Binaries to be used for simulation. Either 32 bit or 64 bit
NETSIM_PATH="C:\\Users\\Ranveer\\Documents\\NetSim_13.0.22_64_std_default\\bin\\bin_x64"

#Set NETSIM_AUTO environment variable to avoid keyboard interrupt at the end of each simulation
os.environ['NETSIM_AUTO'] = '1'

#Create IOPath directory to store the input Configuration.netsim file and the simulation output files during each iteration
if not os.path.exists('IOPath'):
    os.makedirs('IOPath')

#Create Data directory to store the Configuration.netsim and the Metrics.xml files associated with each iteration
if not os.path.exists('Data'):
    os.makedirs('Data')

#Clear the IOPath folder if it has any files created during previous multi-parameter sweep runs
for root, dirs, files in os.walk('IOPath'):
    for file in files:
        os.remove(os.path.join(root, file))

#Clear the Data folder if it has any files created during previous multi-parameter sweep runs
for root, dirs, files in os.walk('Data'):
    for file in files:
        os.remove(os.path.join(root, file))

#Delete result.csv file if it already exists
if(os.path.isfile("result.csv")):
    os.remove("result.csv")

#create a csv file to log the output metrics for analysis
csvfile = open("result.csv", 'w')

#Add headings to the CSV file
csvfile.write('Y,THROUGHPUT(Mbps),')
csvfile.close()

#Iterate based on the number of time simulation needs to be run and the input parameter range
for i in range(250, 401, 50):

    if(os.path.isfile("Configuration.netsim")):
        os.remove("Configuration.netsim")

    if(os.path.isfile("IOPath\Configuration.netsim")):
        os.remove("IOPath\Configuration.netsim")

    if(os.path.isfile("IOPath\Metrics.xml")):
        os.remove("IOPath\Metrics.xml")

    #Call ConfigWriter.exe with arguments as per the number of variable parameters in the input.xml file
    cmd='ConfigWriter.exe '+str(i)
    print(cmd)
    os.system(cmd)

    #Copy the Configuration.netsim file generated by ConfigWriter.exe to IOPath directory 
    if(os.path.isfile("Configuration.netsim")):
        shutil.copy("Configuration.netsim","IOPath\Configuration.netsim")

    #Run NetSim via CLI mode by passing the apppath iopath and license information to the NetSimCore.exe
    cmd=NETSIM_PATH+"\\NetSimcore.exe -apppath "+NETSIM_PATH+" -iopath IOPath -license 5053@192.168.0.9"
    os.system(cmd)
    #print(cmd)

    #Create a copy of the output Metrics.xml file for writing the result log
    if(os.path.isfile("IOPath\Metrics.xml")):
        shutil.copy("IOPath\Metrics.xml","Metrics.xml")

    #Write the value of the variable parameter in the current iteration to the result log
    csvfile = open("result.csv", 'a')
    if(os.path.isfile("Metrics.xml")):
        csvfile.write('\n'+str(i)+',')
        csvfile.close()
        #Call the MetricsReader.exe passing the name of the output log file for updating the log based on script.txt
        os.system("MetricsReader.exe result.csv")

    else:
        #Update the output Metric as crash if Metrics.xml file is missing
        csvfile.write('\n'+str(i)+','+'crash'+',')
        csvfile.close()

    #Create a copy of the Configuration.netsim file appending the value of the variable parameters used in the current iteration
    if(os.path.isfile("Configuration.netsim")):
        shutil.copy("Configuration.netsim", "Data\configuration_"+str(i)+".netsim")

    #Create a copy of the Metrics.xml file appending the value of the variable parameters used in the current iteration
    if(os.path.isfile("Metrics.xml")):
        shutil.copy("Metrics.xml", "Data\metrics_"+str(i)+".xml")

    #Delete Configuration.netsim file created during the last iteration
    if(os.path.isfile("Configuration.netsim")):
        os.remove("Configuration.netsim")

     #Delete Metrics.xml file created during the last iteration
    if(os.path.isfile("Metrics.xml")):
        os.remove("Metrics.xml")
