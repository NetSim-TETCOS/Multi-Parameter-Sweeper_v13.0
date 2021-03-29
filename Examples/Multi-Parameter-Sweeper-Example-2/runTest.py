import random
import shutil
import math
import sys
import os


NETSIM_PATH="C:\\Users\\Ranveer\\Documents\\NetSim_13.0.22_64_std_default\\bin\\bin_x64"
os.environ['NETSIM_AUTO'] = '1'

if not os.path.exists('IOPath'):
    os.makedirs('IOPath')

if not os.path.exists('Data'):
    os.makedirs('Data')
for root, dirs, files in os.walk('Data'):
    for file in files:
        os.remove(os.path.join(root, file))

for root, dirs, files in os.walk('IOPath'):
    for file in files:
        os.remove(os.path.join(root, file))

bandwidth=[10,15,20,25,30,40,50]
Tx_Antenna_count=[8,16,32,64,128]
Rx_Antenna_count = [2,4,8,16]
prb_count=[52,79,106,133,160,216,270]
guard_band=[312.5,382.5,452.5,522.5,592.5,552.5,692.5]

ref_iat=166

if(os.path.isfile("result.csv")):
    os.remove("result.csv")

csvfile = open("result.csv", 'w')
csvfile.write('CHANNELBANDWIDTH_MHz,Tx_ANTENNA_COUNT,RX_ANTENNA_COUNT,INTER_ARRIVAL_TIME(micro sec),THROUGHPUT(Mbps),Data Packets transmitted,')
csvfile.close()

k=0
for i in bandwidth:
    k+=1
    for j in Tx_Antenna_count:
       for z in Rx_Antenna_count:
            iat=ref_iat/((i/10)*(j/2))

            if(os.path.isfile("Configuration.netsim")):
                os.remove("Configuration.netsim")

            if(os.path.isfile("IOPath\Configuration.netsim")):
                os.remove("IOPath\Configuration.netsim")

            if(os.path.isfile("IOPath\Metrics.xml")):
                os.remove("IOPath\Metrics.xml")

            cmd='ConfigWriter.exe '+str(i)+' '+str(j)+' '+str(z)+' '+str(iat)+' '+str(prb_count[k-1])\
            +' '+str(guard_band[k-1])
            print(cmd)
            os.system(cmd)

            if(os.path.isfile("Configuration.netsim")):
                shutil.copy("Configuration.netsim","IOPath\Configuration.netsim")

            cmd=NETSIM_PATH+"\\NetSimcore.exe -apppath "+NETSIM_PATH+" -iopath IOPath -license 5053@192.168.0.9"
            os.system(cmd)
            #print(cmd)

            if(os.path.isfile("IOPath\Metrics.xml")):
                shutil.copy("IOPath\Metrics.xml","Metrics.xml")        

            if(os.path.isfile("Metrics.xml")):
                csvfile = open("result.csv", 'a')
                csvfile.write('\n'+str(i)+','+str(j)+','+str(z)+','+str(iat)+',')            
                os.rename("Script1.txt","Script.txt");
                csvfile.close()
                os.system("MetricsReader.exe result.csv")
                csvfile = open("result.csv", 'a')
                csvfile.write(',')
                csvfile.close()
                os.rename("Script.txt","Script1.txt");
                os.rename("Script2.txt","Script.txt");
                os.system("MetricsReader.exe result.csv")
                os.rename("Script.txt","Script2.txt");

            else:
                csvfile.write('\n'+str(i)+','+str(j)+','+str(iat)+','+'crash'+','+'crash'+',')
                csvfile.close()
            

            if(os.path.isfile("Configuration.netsim")):
                shutil.copy("Configuration.netsim", "Data\configuration_"+str(i)\
                +'_'+str(j)+'_'+str(z)+".netsim")

            if(os.path.isfile("Metrics.xml")):
                shutil.copy("Metrics.xml", "Data\metrics_"+str(i)+'_'+str(j)+'_'+str(z)+".xml")

            if(os.path.isfile("Configuration.netsim")):
                os.remove("Configuration.netsim")

            if(os.path.isfile("Metrics.xml")):
                os.remove("Metrics.xml")
