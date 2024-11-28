from database import *
from indexer import index

## TEST DATA
test_data = [
    "Dr. Salem research activities are tied to 20+ experience in the professional industry. He is very keen on involving his students in his research activities and publishing scholarly work in internationally reputable journals and conferences. His professional experience offered him a wide spectrum of ideas to explore, which benefits his students. Examples of research interests: Performance-based design for special structures, Vulnerability and Risk Assessment of Structures, Soils-Structure Interaction for seismic application, vibration testing and experimental modal analysis of structures and foundation system.",
    "Deep Learning, Data Mining and Statistical Modeling Application of Computer Vision to Civil Engineering Traffic Safety and Operation Transportation-related Environment Public Health",
    "Nonlinear seismic response of flexible buildings and large-span bridges Liquid-Structure Interaction Seismic response of steel frame buildings to near-source ground motions Soil-Structure Interaction Effects on seismic response of structures"
]


# pass in an array of strings to index
index(test_data)