import random
import shutil
import math
import sys
import os


NETSIM_PATH="C:\\Users\\HP\\Documents\\NetSim_13.0.26_64_std_default\\bin\\bin_x64"
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

            cmd=NETSIM_PATH+"\\NetSimcore.exe -apppath "+NETSIM_PATH+" -iopath IOPath -license "+"\"C:\\Program Files\\NetSim\\Standard_v13_0\\bin\"" 
            os.system(cmd)
            #print(cmd)

            if(os.path.isfile("IOPath\Metrics.xml")):
                shutil.copy("IOPath\Metrics.xml","Metrics.xml")        
            
            #Number of Script files i.e Number of Output parameters to be read from Metrics.xml
            #If only one output parameter is to be read only one Script text file with name Script.txt to be provided
            #If more than one output parameter is to be read, multiple Script text file with name Script1.txt, Script2.txt,...
            #...,Scriptn.txt to be provided
            OUTPUT_PARAM_COUNT=2;
            
            if(os.path.isfile("Metrics.xml")):
                #Write the value of the variable parameters in the current iteration to the result log
                csvfile = open("result.csv", 'a')
                csvfile.write('\n'+str(i)+','+str(j)+','+str(z)+','+str(iat)+',')    
                csvfile.close()
                
                if(OUTPUT_PARAM_COUNT==1):
                    #Call the MetricsReader.exe passing the name of the output log file for updating the log based on script.txt
                    os.system("MetricsReader.exe result.csv")                
                else:
                    for n in range(1,OUTPUT_PARAM_COUNT+1,1):
                        os.rename("Script"+str(n)+".txt","Script.txt");
                        os.system("MetricsReader.exe result.csv")
                        csvfile = open("result.csv", 'a')
                        csvfile.write(',')
                        csvfile.close()
                        os.rename("Script.txt","Script"+str(n)+".txt");          
            else:
                csvfile.write('\n'+str(i)+','+str(j)+','+str(iat)+','+'crash'+','+'crash'+',')
                csvfile.close()
            
            #Name of the Output folder to which the results will be saved
            OUTPUT_PATH='Data\\Output_'+str(i)+'_'+str(j)+'_'+str(z);
            
            if not os.path.exists(OUTPUT_PATH):
                os.makedirs(OUTPUT_PATH)

            
            #Create a copy of all files that is present in IOPATH to the desired output location
            files_names = os.listdir('IOPATH')
            for file_name in files_names:
                shutil.move(os.path.join('IOPATH', file_name),OUTPUT_PATH)

            if(os.path.isfile("Configuration.netsim")):
                os.remove("Configuration.netsim")

            if(os.path.isfile("Metrics.xml")):
                os.remove("Metrics.xml")
