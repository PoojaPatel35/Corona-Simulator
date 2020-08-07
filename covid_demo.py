import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from covid import Covid
covid = Covid()
covid.get_data()

countries = covid.list_countries()
print(countries)
us_cases = covid.get_status_by_country_id(18)
print(us_cases)
#Get Total Active cases
active = covid.get_total_active_cases()
#Get Total Confirmed cases
confirmed = covid.get_total_confirmed_cases()
#Get Total Recovered cases
recovered = covid.get_total_recovered()
#Get Total Deaths
deaths = covid.get_total_deaths()
#Getting data from Worldometers.info

covid = Covid(source="worldometers")
#Get Data
covid.get_data()
# print(covid.get_data())
totaldata = covid.get_data()
x = np.linspace(0, 10, 1000)
countries = [sub['country'] for sub in totaldata]
confirm_cases = [sub['confirmed'] for sub in totaldata]
active_cases = [sub['active'] for sub in totaldata]
death_cases =[sub['deaths'] for sub in totaldata]
recovered_cases = [sub['recovered'] for sub in totaldata]
bar_width = 0.35
df_data = pd.DataFrame(covid.get_data())



fina_df = df_data[df_data.confirmed >= 1000000]

melted_df = pd.melt(fina_df, id_vars=['country'], value_vars=['confirmed','active','deaths','recovered'])
print(melted_df)

melted_df.plot.bar(x = 'country')

plt.show()
# plt.bar( countries[:5],recovered_cases[:5],death_cases[:5], color ='b', width=0.25 )
# # plt.bar( countries[:5],death_cases[:5],  color ='g', width=0.25 )
# # plt.bar( countries[:5],confirm_cases[:5], color ='b', width=0.25 )
# # plt.bar( countries[:5],active_cases[:5],  color ='g', width=0.25 )
# plt.title ("COVID - 19 Death vs Recover Cases")
# plt.ylabel ("Number of Cases")
# plt.xlabel("Country name")
# plt.show()
# plt.bar( countries[:5],recovered_cases[:5],  color ='y', width=0.35 )





