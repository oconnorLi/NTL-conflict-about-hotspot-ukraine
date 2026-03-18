from osgeo import gdal, os#VNP42A1\A2 HDFconvertTIF
import numpy as np
from tqdm import tqdm
from time import sleep

input_path="D:\\Download\\"
rasterFiles =os.listdir(input_path)
fileExtension = "_BBOX.tif"

for i in tqdm(range(len(os.listdir(input_path)) - 1)):
    
    rasterFilePre = rasterFiles[i][:-3]#Get File Name Prefix
    hdflayer = gdal.Open(input_path + rasterFiles[i], gdal.GA_ReadOnly)## Open HDF file
    print(hdflayer)
    subhdflayer = (hdflayer.GetSubDatasets()[0][0]) 
    print(subhdflayer)
    rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)
    #outputName = rlayer.GetMetadata_Dict()['long_name']

    #Subset the Long Name
    outputName = subhdflayer[108:] 
    outputNameNoSpace = outputName.strip().replace(" ","_").replace("/","_")

    outputNameFinal = rasterFilePre[0:23] + outputNameNoSpace + fileExtension
    print(outputNameFinal)
    outputFolder = "D:\\Download\\"
    
    outputRaster = outputFolder +  outputNameFinal

    #collect bounding box coordinates
    HorizontalTileNumber = int(rlayer.GetMetadata_Dict()["HorizontalTileNumber"])
    VerticalTileNumber = int(rlayer.GetMetadata_Dict()["VerticalTileNumber"])
    
    WestBoundCoord = (10*HorizontalTileNumber) - 180
    NorthBoundCoord = 90-(10*VerticalTileNumber)
    EastBoundCoord = WestBoundCoord + 10
    SouthBoundCoord = NorthBoundCoord - 10

    EPSG = "-a_srs EPSG:4326" #WGS84

    translateOptionText = EPSG+" -a_ullr " + str(WestBoundCoord) + " " + str(NorthBoundCoord) + " " + str(EastBoundCoord) + " " + str(SouthBoundCoord)

    translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))
    gdal.Translate(outputRaster,rlayer, options=translateoptions)
sleep(0.01)
sleep(0.23)

    #Display image in QGIS (run it within QGIS python Console) - remove comment to display
    #iface.addRasterLayer(outputRaster, outputNameFinal)
    
#A1图层顺序
# =============================================================================
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M12', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M12 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M13', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M13 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M15', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M15 (16-bit unsigned integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M16', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/BrightnessTemperature_M16 (16-bit unsigned integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/DNB_At_Sensor_Radiance_500m', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/DNB_At_Sensor_Radiance_500m (16-bit unsigned integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Glint_Angle', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Glint_Angle (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Granule', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Granule (8-bit unsigned character)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Lunar_Azimuth', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Lunar_Azimuth (16-bit integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Lunar_Zenith', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Lunar_Zenith (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Moon_Illumination_Fraction', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Moon_Illumination_Fraction (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Moon_Phase_Angle', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Moon_Phase_Angle (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_Cloud_Mask', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_Cloud_Mask (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_DNB', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_DNB (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M10', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M10 (16-bit unsigned integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M11', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M11 (16-bit unsigned integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M12', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M12 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M13', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M13 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M15', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M15 (16-bit unsigned integer)'),
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M16', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_VIIRS_M16 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Radiance_M10', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Radiance_M10 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Radiance_M11', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Radiance_M11 (16-bit unsigned integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Sensor_Azimuth', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Sensor_Azimuth (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Sensor_Zenith', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Sensor_Zenith (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Solar_Azimuth', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Solar_Azimuth (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Solar_Zenith', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Solar_Zenith (16-bit integer)'), 
#('HDF5:"VNP46A1.A2023111.h22v03.001.2023112232634.h5"://HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/UTC_Time', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/UTC_Time (32-bit floating-point)')]   
# =============================================================================
#A2图层顺序
# =============================================================================
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/DNB_BRDF-Corrected_NTL', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/DNB_BRDF-Corrected_NTL (16-bit unsigned integer)'), 
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/DNB_Lunar_Irradiance', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/DNB_Lunar_Irradiance (16-bit unsigned integer)'), 
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Gap_Filled_DNB_BRDF-Corrected_NTL', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Gap_Filled_DNB_BRDF-Corrected_NTL (16-bit unsigned integer)'), 
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Latest_High_Quality_Retrieval', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Latest_High_Quality_Retrieval (8-bit unsigned character)'), 
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Mandatory_Quality_Flag', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Mandatory_Quality_Flag (8-bit unsigned character)'), 
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_Cloud_Mask', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/QF_Cloud_Mask (16-bit unsigned integer)'), 
# HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Snow_Flag', '[2400x2400] //HDFEOS/GRIDS/VNP_Grid_DNB/Data_Fields/Snow_Flag (8-bit unsigned character)')]
# =============================================================================
