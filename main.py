from database import *
from indexer import index

## TEST DATA
test_data = [
    "Dr. Salem research activities are tied to 20+ experience in the professional industry. He is very keen on involving his students in his research activities and publishing scholarly work in internationally reputable journals and conferences. His professional experience offered him a wide spectrum of ideas to explore, which benefits his students. Examples of research interests: Performance-based design for special structures, Vulnerability and Risk Assessment of Structures, Soils-Structure Interaction for seismic application, vibration testing and experimental modal analysis of structures and foundation system.",
    "Deep Learning, Data Mining and Statistical Modeling Application of Computer Vision to Civil Engineering Traffic Safety and Operation Transportation-related Environment Public Health",
    "Nonlinear seismic response of flexible buildings and large-span bridges Liquid-Structure Interaction Seismic response of steel frame buildings to near-source ground motions Soil-Structure Interaction Effects on seismic response of structures"
]

test_data2 = [
    "Tropical fish include fish found in tropical environments around the world, including both freshwater and salt water species.",
    "Fishkeepers often use the term tropical fish to refer only those requiring fresh water, with saltwater tropical fish referred to as marine fish.",
    "Tropical fish are popular aquarium fish, due to their often bright coloration.",
    "In freshwater fish, this coloration typically derives from iridescence, while salt water fish are generally pigmented."
]

test_data3 = {
    "https://www.cpp.edu/faculty/ysalem": "Dr. Salem research activities are tied to 20+ experience in the professional industry. He is very keen on involving his students in his research activities and publishing scholarly work in internationally reputable journals and conferences. His professional experience offered him a wide spectrum of ideas to explore, which benefits his students. Examples of research interests: Performance-based design for special structures, Vulnerability and Risk Assessment of Structures, Soils-Structure Interaction for seismic application, vibration testing and experimental modal analysis of structures and foundation system.",
    "https://www.cpp.edu/faculty/wcheng": "Deep Learning, Data Mining and Statistical Modeling Application of Computer Vision to Civil Engineering Traffic Safety and Operation Transportation-related Environment Public Health",
    "https://www.cpp.edu/faculty/ylwang": "Nonlinear seismic response of flexible buildings and large-span bridges Liquid-Structure Interaction Seismic response of steel frame buildings to near-source ground motions Soil-Structure Interaction Effects on seismic response of structures"
}

test_data4 = {
    "https://test.com/0": "Tropical fish include fish found in tropical environments around the world, including both freshwater and salt water species.",
    "https://test.com/1": "Fishkeepers often use the term tropical fish to refer only those requiring fresh water, with saltwater tropical fish referred to as marine fish.",
    "https://test.com/2": "Tropical fish are popular aquarium fish, due to their often bright coloration.",
    "https://test.com/3": "In freshwater fish, this coloration typically derives from iridescence, while salt water fish are generally pigmented."
}

# pass in an array of strings to index
index(test_data4)