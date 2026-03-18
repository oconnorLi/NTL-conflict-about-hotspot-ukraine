# NTL-conflict-about-hotspot-ukraine
The Application of NTL in Conflict events
I. Data
1. Due to the large volume of data involved in this paper, all data can be downloaded directly from the URL provided in the "Auxiliary Data" section of the manuscript.
2. The NTL source data ("Origin data"), Hotspot result data ("Hotspot_result"), the ACLED conflict data used in the study ("ACLED"), and selected geospatial data ("valid_data") are available for download via the shared cloud drive link: Data.
Link: https://pan.baidu.com/s/1hHA5XLW7Oy76kEMsWW5dOg | Extraction Code: ymfw
II. Processing Tools
1. The ISODATA results were generated using the ISODATA module within the ENVI 5.6.2 user interface (UI); this module was applied to the pre-processed NTL imagery to derive the Hotspot results, utilizing the specific parameter settings detailed in the paper.
2. All thematic maps presented in the paper were created using ArcGIS 10.8; flowcharts were generated using Visio, while other statistical charts were produced using Origin and Python.
3. The high-resolution optical imagery used for the Hotspot maps in the paper was sourced from Google Earth Pro.
III. Relevant Code
Located in the "code" folder:
`discussion_data.py` corresponds to Figure 17.
`HDF5_product_to_GeoTiff.py` is used to convert the source HDF5 data into a processable GeoTIFF format.
`Quality_DNB.py` corresponds to Figure 18.
`scatter.py` corresponds to Figure 4.
`scatter_paper.py` corresponds to Figure 13.
