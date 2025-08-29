from  Parameters import * 

import  numpy as np

import  matplotlib.pyplot as plt


label='ARM_1997_E13'
#label='ARM_1997_E2'
file1= open('%s/soil_%s'%(path,label)  ,'w+')
file1.write("Thickness[m]\tSoilt[K]\tWetness[%]\tSand[%]\tClay[%]\tRelax Function\n")
print("Thickness[m]\tSoilt[K]\tWetness[%]\tSAND[%]\tCLAY[%]\tRelax Function\n")

thikness=[]

for i in range(0,len(yn)-1):

    #print(target_depths[i+1]-target_depths[i])
    thikness.append(yn[i+1]-yn[i])


#hour
time=5

for j in range(0,len(yn)):

    #file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(thikness[j]/100.0,mean_t[time,j]+273.15,mean_q[time,j],soil.sand[j],soil.clay[j],0))
    #print("%f\t%f\t%f\t%f\t%f\t%f\n"%(thikness[j]/100.0,mean_t[time,j]+273.15,mean_q[time,j],soil.sand[j],soil.clay[j],0))
    file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(yn[j]/100.0,mean_t[time,j]+273.15,mean_q[time,j],soil.sand[j],soil.clay[j],0))
    print("%f\t%f\t%f\t%f\t%f\t%f\n"%(yn[j]/100.0,mean_t[time,j]+273.15,mean_q[time,j],soil.sand[j],soil.clay[j],0))

file1.close()
