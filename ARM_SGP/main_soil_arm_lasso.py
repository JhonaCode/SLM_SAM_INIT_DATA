from  Parameters_arm_lasso import * 

import  numpy as np

import  matplotlib.pyplot as plt


label='ARM_lasso'
file1= open('%s/soil_%s'%(path,label)  ,'w+')
file1.write("Thickness[m]\tSoilt[K]\tWetness[%]\tSand[%]\tClay[%]\tRelax Function\n")
print("Thickness[m]\tSoilt[K]\tWetness[%]\tSAND[%]\tCLAY[%]\tRelax Function\n")

#print(meantT.depth)
thikness=[]

for i in range(0,len(meantime.depth)-1):

    #print(target_depths[i+1]-target_depths[i])
    thikness.append(meantime.depth[i+1]-meantime.depth[i])


for j in range(0,len(meantime.depth)):

    file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(meantime.depth[j]/100.0,meantime.T[j],meantime.W[j],soil.sand[j],soil.clay[j],0))
    print("%f\t%f\t%f\t%f\t%f\t%f\n"%(meantime.depth[j]/100.0,meantime.T[j],meantime.W[j],soil.sand[j],soil.clay[j],0))

file1.close()

y=[]
for i in range(0,len(target_depths)-1):

    print(target_depths[i+1]-target_depths[i])
    y.append(target_depths[i+1]-target_depths[i])


file1= open('%s/soil_interpolation_%s'%(path,label)  ,'w+')
file1.write("Thickness[m]\tSoilt[K]\tWetness[%]\tSand[%]\tClay[%]\tRelax Function\n")
#print('inter')

for j in range(0,len(target_depths)):

    file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[j]/100.0,mean_t[j],mean_q[j],soil.sand[j],soil.clay[j],0))
    print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[j]/100.0,mean_t[j],mean_q[j],soil.sand[j],soil.clay[j],0))



file1.close()
