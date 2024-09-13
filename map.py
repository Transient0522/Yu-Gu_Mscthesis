import geopandas
from parse_data import init_data
import matplotlib.pyplot as plt

msoas = geopandas.read_file("./datas/msoa/Middle_Layer_Super_Output_Areas_December_2011_Generalised_Clipped_Boundaries_in_England_and_Wales.shp")
se_dict = init_data()
msoas.info()

msoa_list = list(msoas.get('msoa11cd'))
loc = [i for i in range(len(msoa_list))]
covid_data = [None for _ in range(len(msoa_list))]
imd_data = [None for _ in range(len(msoa_list))]
for i in range(len(msoa_list)):
    if msoa_list[i] in se_dict:
        covid_data[i] = sum(se_dict[msoa_list[i]]['covid'])
        imd_data[i] = se_dict[msoa_list[i]]['imd']

msoas.insert(0, 'covid_sum', covid_data)
msoas.insert(0, 'imd', imd_data)
msoas.info()

# Plot the 'covid_sum' data
msoas.plot("covid_sum", legend=True, vmax=600)
plt.title("COVID-19 Cases by MSOA")
plt.show()

# Plot the 'imd' data
msoas.plot("imd", legend=True, vmax=30)
plt.title("Index of Multiple Deprivation by MSOA")
plt.show()




