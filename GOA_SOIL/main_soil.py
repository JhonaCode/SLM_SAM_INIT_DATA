from  Parameters import * 

import  numpy as np

import  matplotlib.pyplot as plt


soiltype="PastureA" 
#soiltype="Forest" 
#month="Jan"
month="Sep"


label='GOA_itacaiunas_%s_%s'%(soiltype,month)
file1= open('%s/soil_%s'%(path,label)  ,'w+')
file1.write("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
print("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSAND[%]\tCLAY[%]\tRelax Function\n")

thikness=[]

for i in range(0,len(target_depths)-1):

    #print(target_depths[i+1]-target_depths[i])
    thikness.append(target_depths[i+1]-target_depths[i])


#taking from Estimation and mapping of field capacity in Brazilian soils
#https://www.sciencedirect.com/science/article/pii/S0016706120301300?via%3Dihub  
#https://doi.org/10.1016/j.geoderma.2020.114557
Fc=0.38

target_depths[0]=0.001

#for j in range(0,len(thikness)):
for j in range(0,len(target_depths)):

    #file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[j]/100.0,soil_T[soiltype][month][j]+273.15,soil_M[soiltype][month][j]/(100.0*Fc),soil_text[soiltype]["sand"]*100,soil_text[soiltype]["clay"]*100,0))
    print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[j]/100.0,soil_T[soiltype][month][j]+273.15,soil_M[soiltype][month][j]/(100.0*Fc),soil_text[soiltype]["sand"]*100,soil_text[soiltype]["clay"]*100,0))

file1.close()
