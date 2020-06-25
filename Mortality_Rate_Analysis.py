import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid", color_codes=True)


os.chdir("C:/Users/rajku/Downloads/chsi_dataset/")

def birth_death_ratio(df, df2):
    df1 = df[["CHSI_County_Name", "CHSI_State_Name", "White", "Black", "Native_American", "Asian", "Hispanic", "Poverty", "Population_Size"]]
    df_1 = df1[df1["Poverty"]>=0].copy()
    df_1['Others'] = df_1['Native_American']+df_1['Asian']
    df_1 = df_1.drop(["Native_American", "Asian"], axis=1)
    birth_death = df2[["CHSI_County_Name", "CHSI_State_Name", "Total_Births", "Total_Deaths"]].copy()
    birth_death = birth_death.loc[(birth_death["Total_Births"] >= 0) & (birth_death["Total_Deaths"] >= 0)]
    birth_death["birth_death_ratio"] = birth_death['Total_Deaths']/birth_death['Total_Births']*100
    data = pd.merge(df_1, birth_death, on = ['CHSI_County_Name', 'CHSI_State_Name'])
    data = data.round(2)
    pd.set_option('display.max_columns', None)
    print(data.sort_values(by = 'Poverty',ascending=False))

    dfa = df_1.groupby(["CHSI_State_Name"], as_index=False).agg(
        {"White": "mean", "Black": "mean", "Others": "mean", "Hispanic": "mean", "Poverty": "mean"})
    dfb = birth_death.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Births": "mean", "Total_Deaths": "mean"})
    final_df = pd.merge(dfa, dfb, on="CHSI_State_Name")
    final_df = final_df.round(2)
    final_df = final_df.sort_values(by=["Poverty"], ascending=False)
    print(final_df)

    plt.subplot(2, 1, 1)
    plt.scatter(x=data['Poverty'], y=data["White"], color="DarkGreen", label="White")
    plt.scatter(x=data['Poverty'], y=data["Black"], color="DarkBlue", label="Black")
    plt.scatter(x=data['Poverty'], y=data["Others"], color="Red", label="Others")
    plt.scatter(x=data['Poverty'], y=data["Hispanic"], color="Orange", label="Hispanic")
    plt.xlabel("Poverty")
    plt.ylabel("Race-wise Pop")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.title("County & Race-wise Poverty")
    plt.grid(linewidth=0.5, color = "grey")

    plt.subplot(2, 1, 2)
    plt.scatter(x=final_df['Poverty'], y=final_df["White"], color="DarkGreen", label="White")
    plt.scatter(x=final_df['Poverty'], y=final_df["Black"], color="DarkBlue", label="Black")
    plt.scatter(x=final_df['Poverty'], y=final_df["Others"], color="Red", label="Others")
    plt.scatter(x=final_df['Poverty'], y=final_df["Hispanic"], color="Orange", label="Hispanic")
    plt.xlabel("Poverty")
    plt.ylabel("Race-wise Pop")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.grid(linewidth=0.5, color="grey")
    plt.title("State & Race-wise Poverty")
    plt.show()


def population_poverty(df):
    df1 = df[["CHSI_State_Name", "Poverty", "Population_Size"]]
    df1 = df1[df1["Poverty"]>=0]
    df_2 = df1.groupby(["CHSI_State_Name"], as_index=False).agg({"Population_Size":"mean", "Poverty":"mean"})
    df_2["Pop_Poverty_ratio"] = df_2["Population_Size"]/df_2["Poverty"]
    df_2 = df_2.sort_values(by=["Pop_Poverty_ratio"], ascending=True)

    df_3 = df_2.head(10)
    df_4 = df_2.tail(10)


def death_factors(df1, df2):
    df = df1[["CHSI_State_Name", "White", "Black", "Native_American", "Asian", "Hispanic"]]
    df_2 = df2[["CHSI_State_Name","Total_Deaths"]]
    df_1 = df.copy()
    df_3 = df_2.copy()
    df_1["Others"] = df_1['Native_American']+df_1['Asian']
    df_1 = df_1.drop(["Native_American", "Asian"], axis=1)
    population = df_1.groupby(["CHSI_State_Name"], as_index=False).agg({"Black":"mean", "White":"mean", "Others":"mean", "Hispanic":"mean"})
    population = population.round(2)
    deaths = df_2.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Deaths":"mean"})
    deaths = deaths.round(0)
    pop_deaths = pd.merge(population, deaths, on="CHSI_State_Name")
    pop_deaths = pop_deaths.sort_values(by=["Total_Deaths"], ascending=False)
    first_20 = pop_deaths.head(10)
    last_20 = pop_deaths.tail(10)
    print(first_20)
    print(last_20)

    p1 = plt.bar(first_20["CHSI_State_Name"], first_20["White"], width=1, color="DarkGreen", edgecolor="black", label="White")
    p2 = plt.bar(first_20["CHSI_State_Name"], first_20["Black"], width=1, bottom=first_20["White"], color="Blue", edgecolor="black", label="Black")
    p3 = plt.bar(first_20["CHSI_State_Name"], first_20["Others"], width=1, bottom=np.array(first_20["White"]) + np.array(first_20["Black"]),
                 color="Red", edgecolor="black", label="Others")
    p4 = plt.bar(first_20["CHSI_State_Name"], first_20["Hispanic"], width=1,
                 bottom=np.array(first_20["White"]) + np.array(first_20["Black"]) + np.array(first_20["Others"]),
                 color="Orange", edgecolor="black", label="Hispanic")

    r1 = plt.bar(last_20["CHSI_State_Name"], last_20["White"], width=1, color="DarkGreen", edgecolor="black")
    r2 = plt.bar(last_20["CHSI_State_Name"], last_20["Black"], width=1, bottom=last_20["White"], color="Blue", edgecolor="black")
    r3 = plt.bar(last_20["CHSI_State_Name"], last_20["Others"], width=1,
                 bottom=np.array(last_20["White"]) + np.array(last_20["Black"]),
                 color="Red", edgecolor="black")
    r4 = plt.bar(last_20["CHSI_State_Name"], last_20["Hispanic"], width=1,
                 bottom=np.array(last_20["White"]) + np.array(last_20["Black"]) + np.array(last_20["Others"]),
                 color="Orange", edgecolor="black")

    plt.xlabel("Top & Last 10 States")
    plt.ylabel("Race-wise Pop percent")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.xticks(rotation="vertical")
    plt.grid(linewidth=0.5, color = "grey")
    plt.title("Top 10 & last 10 states ")
    plt.show()


def age_poverty(df):
    """The state wise output shoews that the percent of population for Age_85_and_Over is slightly greater in top 10 states with Low Poerty index
    as compared to that of states with high poverty index"""
    df_1 = df[["CHSI_County_Name", "CHSI_State_Name", "Age_19_Under", "Age_19_64", "Age_65_84", "Age_85_and_Over", "Poverty"]]
    df_1 = df_1.replace([-1111.1, -2222.2], np.nan)
    df_2 = df_1.groupby(["CHSI_County_Name","CHSI_State_Name"], as_index=False)["Age_19_Under", "Age_19_64", "Age_65_84", "Age_85_and_Over", "Poverty"].mean()
    df_3 = df_2.sort_values(by="Poverty", ascending=False)
    df_3 = df_3.round(2)
    # print(df_3.head(10))
    # print(df_3.tail(10))

    df_4 = df_1.groupby(["CHSI_State_Name"], as_index=False)["Age_19_Under", "Age_19_64", "Age_65_84", "Age_85_and_Over", "Poverty"].mean()
    df_5 = df_4.sort_values(by="Poverty", ascending=False)
    df_5 = df_5.round(2)
    # print(df_5.head(10))
    # print(df_5.tail(10))





def merge_dataframes(dataframe1, dataframe2, dataframe3, dataframe4):
    df_demo = dataframe2[["CHSI_County_Name","CHSI_State_Name","Poverty","Population_Size"]]
    df_riskfactor = dataframe1[["CHSI_County_Name","CHSI_State_Name","No_Exercise","Obesity","High_Blood_Pres","Few_Fruit_Veg","Smoker","Diabetes","Uninsured","Elderly_Medicare","Disabled_Medicare","Prim_Care_Phys_Rate"]]
    df_measurebd = dataframe3[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","Late_Care","Infant_Mortality","Total_Deaths","Total_Births"]]
    df_unemp = dataframe4[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","Unemployed"]]
    df_demo_risk = pd.merge(df_demo, df_riskfactor, on=['CHSI_State_Name','CHSI_County_Name'])
    df_demo_risk_bd = pd.merge(df_demo_risk, df_measurebd, on=['CHSI_State_Name','CHSI_County_Name'])
    df_demo_risk_bd_unemp = pd.merge (df_demo_risk_bd, df_unemp, on=['CHSI_State_Name','CHSI_County_Name'])

    pd.set_option('display.max_columns', None)

    return df_demo_risk_bd_unemp


def analysis_1(df):

    df_final_1 = df.replace([-1111, -1111.1, -1, -2222.2, -2222, -2], np.nan)
    df_1 = df_final_1[["CHSI_County_Name", "CHSI_State_Name", "Population_Size" , "Poverty", "Total_Deaths", "No_Exercise","Obesity", "Few_Fruit_Veg", "Smoker", "Diabetes", "High_Blood_Pres"]]
    df_1 = df_1.groupby(["CHSI_State_Name"], as_index=False)["Poverty", "Total_Deaths", "Population_Size", "No_Exercise", "Obesity", "Few_Fruit_Veg", "Smoker",  "Diabetes", "High_Blood_Pres"].mean()
    df_1 = df_1.sort_values(by=["Poverty", "Total_Deaths"], ascending=False)
    df_1 = df_1.round(2)
    #print(df_1.head(10))

    df_2 = df_final_1[["CHSI_County_Name", "CHSI_State_Name", "Population_Size" , "Poverty", "Uninsured", "Elderly_Medicare", "Disabled_Medicare", "Late_Care", "Prim_Care_Phys_Rate", "Total_Deaths"]]
    df_2 = df_2.groupby(["CHSI_State_Name"], as_index=False)["Population_Size" , "Poverty", "Uninsured", "Elderly_Medicare", "Disabled_Medicare", "Late_Care","Prim_Care_Phys_Rate", "Total_Deaths"].mean()
    df_2 = df_2.sort_values(by=["Poverty", "Total_Deaths"], ascending=False)
    df_2 = df_2.round(2)
    pd.set_option('display.max_columns', None)
    df_2 = df_2.dropna()
    sns.heatmap(df_2.corr(), xticklabels=df_2.corr().columns, yticklabels=df_2.corr().columns, cmap='RdYlGn', center=0, annot=True)
    plt.title('Correlogram of Poverty', fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()
    #print(df_2.head(10))


def other_risk_factors(df1, df2):
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "LBW", "VLBW", "Premature", "Under_18", "Over_40", "Late_Care", "Total_Births", "Total_Deaths"]]
    df_1 = df_1.replace([-1111.1, -2222.2], np.nan)
    df_1["Birth_Death_Ratio"] = df_1["Total_Deaths"]/df_1["Total_Births"]*100
    df_1["LBW_VLBW"] = df_1["LBW"] + df_1["VLBW"]
    df_1 = df_1.drop(["Total_Deaths", "Total_Births", "LBW", "VLBW"], axis=1)
    df_2 = df2[["CHSI_County_Name", "CHSI_State_Name", "Poverty", "Population_Size"]]
    df_2 = df_2.replace([-1111.1, -2222.2], np.nan)
    df_3 = pd.merge(df_1, df_2, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_3 = df_3.sort_values(by=["Poverty", "Birth_Death_Ratio"], ascending=[False, False])
    print(df_3.head(20))
    print(df_3.tail(20))

    df_4 = df_3.groupby(["CHSI_State_Name"], as_index=False)["Premature", "Under_18", "Over_40", "Late_Care", "LBW_VLBW", "Birth_Death_Ratio", "Poverty"].mean()
    df_4 = df_4.sort_values(by=["Poverty", "Birth_Death_Ratio"], ascending=[False, False])
    df_4 = df_4.round(2)
    # print(df_4.head(10))
    # print(df_4.tail(10))

    df_5 = df_4.head(10)
    df_6 = df_4.tail(10)
    df_7 = pd.concat([df_5, df_6])
    print(df_7)
    plt.subplot(2,2,1)
    plt.bar(df_7["CHSI_State_Name"], df_7["Poverty"])
    plt.ylabel("Statewise Poverty")
    plt.xticks([])


    plt.subplot(2,2,3)
    plt.bar(df_7["CHSI_State_Name"], df_7["Under_18"])
    plt.ylabel("Under_18_births")
    plt.xticks(df_7["CHSI_State_Name"], rotation="vertical")

    plt.subplot(2, 2, 2)
    plt.bar(df_7["CHSI_State_Name"], df_7["Premature"])
    plt.ylabel("Premature_births")
    plt.xticks([])

    plt.subplot(2, 2, 4)
    under_18 = plt.bar(df_7["CHSI_State_Name"], df_7["Late_Care"])
    plt.ylabel("Late_Care_births")
    plt.xticks(df_7["CHSI_State_Name"], rotation="vertical")

    plt.show()


def genetic_deaths(df1,df2):
    df = pd.merge(df1,df2, on = ["CHSI_County_Name","County_FIPS_Code","CHSI_State_Name","State_FIPS_Code"])
    df_1 = df[['CHSI_State_Name', "A_Wh_BirthDef","A_Bl_BirthDef","A_Ot_BirthDef","A_Hi_BirthDef","Total_Births"]]
    df_1 = df_1.replace([-9999, -2222, -2222.2, -2, -1111.1, -1111, -1], np.nan)
    df_1 = df_1.groupby("CHSI_State_Name")["A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef", "Total_Births"].sum()
    df_1.reset_index()
    pd.set_option('display.max_columns', None)
    #print(df_1)


def air_quality_death(df1, df2, df3):
    df_3 = df3[["CHSI_County_Name", "CHSI_State_Name", "Population_Size"]]
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "Total_Deaths"]]
    df4 = pd.merge(df_1, df_3, on=["CHSI_County_Name", "CHSI_State_Name"])
    df4["Pop_death_ratio"] = df4["Total_Deaths"]/df4["Population_Size"]*100
    df4 = df4.drop(["Population_Size", "Total_Deaths"], axis=1)
    df4 = df4.round(2)
    df4.columns = ["County", "State", "Pop_death_ratio"]
    df4 = df4[df4["Pop_death_ratio"] > 0]
    (df4.sort_values(by="Pop_death_ratio", ascending=True))
    df_2 = df2[["County", "State", "Max AQI", "Unhealthy Days", "Very Unhealthy Days", "Hazardous Days"]]
    data = pd.merge(df4, df_2, on = ["County", "State"])
    data_1 = data.sort_values(by=["Hazardous Days", "Very Unhealthy Days", "Unhealthy Days"], ascending=[False, False, False])
    print(data_1.head(15))
    print(data_1.tail(15))
    df_4 = data_1.head(15)
    df_5 = data_1.tail(15)
    df_6 = pd.concat([df_4, df_5])
    df_6["Total_Unhealthy_days"] = df_6["Hazardous Days"] + df_6["Unhealthy Days"] + df_6["Very Unhealthy Days"]
    df_6.drop(["Hazardous Days", "Very Unhealthy Days", "Unhealthy Days"], axis=1)
    sns.scatterplot(x=df_6["State"], y=df_6["Pop_death_ratio"], size=df_6["Total_Unhealthy_days"], data=df_6)
    plt.xticks(rotation="vertical")
    plt.legend(loc="upper left", fontsize="x-small")
    plt.title("")

    plt.show()



def disease_pollution(df1, df2, df3, df4):
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name","Lung_Cancer", "Brst_Cancer", "Col_Cancer"]]
    df_1 = df_1[(df_1["Lung_Cancer"] > 0) & (df_1["Brst_Cancer"] > 0) & (df_1["Col_Cancer"] > 0)]
    #print(df_1.sort_values(by="Brst_Cancer", ascending=True))
    df_2 = df2[["County", "State", "Max AQI"]]
    df_3 = df3[["CHSI_County_Name", "CHSI_State_Name", "Toxic_Chem"]]
    df_3 = df_3[df_3["Toxic_Chem"] > 0]
    df_4 = df4[["CHSI_County_Name", "CHSI_State_Name", "Population_Size"]]
    df_5 = pd.merge(df_1, df_4, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_5["Lung_Cancer_d"] = (df_5["Lung_Cancer"]*df_5["Population_Size"])/100000
    df_5["Brst_cancer_d"] = (df_5["Brst_Cancer"] * df_5["Population_Size"]) / 100000
    df_5["Col_cancer_d"] = (df_5["Col_Cancer"] * df_5["Population_Size"]) / 100000
    df_5 = df_5.drop(["Lung_Cancer", "Brst_Cancer", "Col_Cancer"], axis=1)
    df_5 = df_5.round()
    df_5["Total_cancer_deaths"] = df_5["Lung_Cancer_d"] + df_5["Brst_cancer_d"] + df_5["Col_cancer_d"]
    #print(df_5.head(10))
    df_6 = pd.merge(df_5, df_3, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_6.columns = ["County", "State", "Population_Size", "Lung_Cancer_d", "Brst_cancer_d", "Col_cancer_d", "Total_cancer_deaths", "Toxic_Chem"]
    df_7 = pd.merge(df_6, df_2, on=["County", "State"])
    df_7 = df_7.sort_values(by=["Toxic_Chem", "Max AQI"], ascending=[False, False])
    print(df_7.head(10))
    print(df_7.tail(10))

#plotting
    df_8 = df_7.head(7)
    df_9 = df_7.tail(7)
    df_10 = pd.concat([df_8, df_9])
    plt.subplot(2,2,1)
    plt.scatter(x=df_10["County"], y=df_10["Total_cancer_deaths"], color="c")
    plt.plot(x=df_10["County"], y=df_10["Total_cancer_deaths"], color="c")
    plt.xticks(rotation="vertical")
    plt.ylabel("Cancer_deaths")
    plt.title("Total cancer deaths for top & last 10 counties")

    plt.subplot(2, 2, 2)
    plt.scatter(x=df_10["County"], y=df_10["Max AQI"], color="m")
    plt.plot(x=df_10["County"], y=df_10["Max AQI"], color="m")
    plt.xticks(rotation="vertical")
    plt.ylabel("Max AQI")
    plt.title("Max AQI for top & last 10 counties")

    plt.subplot(2, 2, 3)
    plt.scatter(x=df_10["County"], y=df_10["Toxic_Chem"], color="darkgreen")
    plt.plot(x=df_10["County"], y=df_10["Toxic_Chem"], color="darkgreen")
    plt.xticks(rotation="vertical")
    plt.ylabel("Toxic Chemicals")
    plt.title("Toxic Chemicals for top & last 10 counties")

    plt.show()



def death_other_factors(df1, df2, df3, df):
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "Major_Depression", "Unemployed", "Recent_Drug_Use"]]
    df_1 = df_1[df_1["Unemployed"] > 0]
    df_2 = df2[["CHSI_County_Name", "CHSI_State_Name", "Suicide", "Homicide"]]
    df_2 = df_2[(df_2["Suicide"] > 0) & (df_2["Homicide"] > 0)]
    df_3 = df3[["CHSI_County_Name", "CHSI_State_Name", "Population_Size", "Poverty"]]
    df_3 = df_3[df_3["Poverty"] > 0]
    df4 = df[["CHSI_County_Name", "CHSI_State_Name", "Total_Deaths"]]
    df_4 = pd.merge(df_2, df_3, on= ["CHSI_County_Name", "CHSI_State_Name"])
    df_4["Deaths_Suicide"] = (df_4["Suicide"] * df_4["Population_Size"])/100000
    df_4["Deaths_Homicide"] = (df_4["Homicide"] * df_4["Population_Size"]) / 100000
    df_4["Poverty_Pop"] = (df_4["Poverty"] * df_4["Population_Size"])/100
    df_4 = df_4.drop(["Homicide", "Suicide", "Poverty"], axis=1)
    df_4 = df_4.round()
    df_5 = pd.merge(df_1, df_4, on =["CHSI_County_Name", "CHSI_State_Name"])
    df_6 = pd.merge(df4, df_5, on =["CHSI_County_Name", "CHSI_State_Name"])
    df_6 = df_6.sort_values(["Poverty_Pop"], ascending=False)
    #print(df_6.head(10))



def read_dataframes():
    demographics = pd.read_csv("DEMOGRAPHICS.csv")
    lead_death_cause = pd.read_csv("LEADINGCAUSESOFDEATH.csv")
    birth_death_measure = pd.read_csv("MEASURESOFBIRTHANDDEATH.csv")
    risk_factors = pd.read_csv("RISKFACTORSANDACCESSTOCARE.csv")
    vulnerable_pops = pd.read_csv("VUNERABLEPOPSANDENVHEALTH.csv")
    air_quality = pd.read_csv("annual_aqi_by_county_2010.csv")
    return demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops, air_quality


if __name__ == '__main__':

    demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops, air_quality  = read_dataframes()
    birth_death_ratio(demographics, birth_death_measure)
    population_poverty(demographics)
    death_factors(demographics, birth_death_measure)
    age_poverty(demographics)
    result = merge_dataframes(risk_factors, demographics, birth_death_measure, vulnerable_pops)
    analysis_1(result)
    other_risk_factors(birth_death_measure, demographics)
    genetic_deaths(lead_death_cause, birth_death_measure)
    air_quality_death(birth_death_measure, air_quality, demographics)
    disease_pollution(birth_death_measure, air_quality, vulnerable_pops, demographics)
    death_other_factors(vulnerable_pops, birth_death_measure, demographics, birth_death_measure)
