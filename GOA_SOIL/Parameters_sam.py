# -*- coding: UTF-8 -*-
###################################################
#PYTHON CODE TO PLOT DIFFERENS
#MPAS DATA USING CARTOPY AND XARRAY.
###################################################
#PYTHON CODE TO PLOT DIFFERENS
#End=`date +%s.%N`
###################################################
# By: Jhonatan A. A Manco
###################################################
# Function to load the complete ncfiles  of regional MONAN run
from   sam_python  import data_own as down

#note   =                                                           
tu      = ['days  since 2025-01-01 00:00:00 +00:00:00','gregorian'] 
exp_name        = 'shca_cass_1'           
path_shca_cass  = '/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/OUT_STAT/GOAMAZON_LES_shca_cass_512x512_50m_400_20m_1s_SAM1MOM.nc'
shca_cass       = down.data_load_xr(path_shca_cass, exp_name, tu)

#-----------------------------------------------------
#note   = 
tu      = ['days  since 2025-01-01 00:00:00 +00:00:00','gregorian']
exp_name        = 'iop2'
path_iop2       = '/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/OUT_STAT/GOAMAZON_LES_iop2_512x512_50m_400_20m_1s_SAM1MOM_z235_cass.nc'
iop2    = down.data_load_xr(path_iop2, exp_name, tu)

#-----------------------------------------------------
#note   = 
tu      = ['days  since 2025-01-01 00:00:00 +00:00:00','gregorian']
exp_name        = 'iop1'
path_iop1_mom   = '/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/OUT_STAT/GOAMAZON_LES_iop1_512x512_50m_400_20m_1s_SAM1MOM_z235_presc_momem_cass.nc'
iop1        = down.data_load_xr(path_iop1_mom, exp_name, tu)


#SHCA
#-----------------------------------------------------
#note   = composto goamazon shca_plat_5h_tk_nearest_modi_512 50m vertical 20m  1 seg micro SAM tke1/5 momemtum prescribed, with the atto soil parameters, meaning in thye complete iop2, and for the 5h (not 6) of the morning
tu      = ['days  since 2025-01-01 00:00:00 +04:00:00','gregorian']
exp_name        = 'shca_plat_nearest_modi'
path_shca_plat_5h_tk_nearest_modi_512   = '/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/OUT_STAT/GOAMAZON/GOAMAZON_shca_512_50m_400_20m_1s_shca_soil_plateaus_5h_tk_nearest_9l_rf_rcm150_z037_alp4_.nc'
shca_plat_nearest_modi  = down.data_load_xr(path_shca_plat_5h_tk_nearest_modi_512, exp_name, tu)


#o mesmo que 
#cass_512_presc
#en Parameters_Cass
#note   = composto cass cass_512_presc prescribed 50m vertical 20m  1 seg micro SAM tke1/5 momemtum prescribed
tu      = ['days  since 2024-12-31 00:00:00 +06:00:00','gregorian']
exp_name        = 'cass'                             
path_cass_512_presc     = '/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/OUT_STAT/CASS/CASS_512_512x512_50m_400_20m_1s_SAM1MOM_tke_false_pres.nc'
cass    = down.data_load_xr(path_cass_512_presc, exp_name, tu)

#-----------------------------------------------------
#note   = 
tu      = ['days  since 2025-01-01 00:00:00 +00:00:00','gregorian']
exp_name        = 'shca_2shf'
path_shca_2shf  = '/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/OUT_STAT/GOAMAZON_LES_shca_2shf_512x512_50m_400_20m_1s_SAM1MOM_z235_presc_momem_cass.nc'
shca_2shf       = down.data_load_xr(path_shca_2shf, exp_name, tu)



