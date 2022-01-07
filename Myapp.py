import numpy as np
import plotly_express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler

df= pd.read_csv("https://raw.githubusercontent.com/Xavicat14/Income-in-South-Korea/main/Korea%20Income%20and%20Welfare.csv")

df=df.drop(df[df.income <0].index)

#region (codificamos correctamente todos los datos)
df.loc[df['region'] == 1, 'region'] = 'Seoul'
df.loc[df['region'] == 2, 'region'] = 'Kyeong-gi'
df.loc[df['region'] == 3, 'region'] = 'Kyoung-nam'
df.loc[df['region'] == 4, 'region'] = 'Kyong-buk'
df.loc[df['region'] == 5, 'region'] = 'Chong-nam'
df.loc[df['region'] == 6, 'region'] = 'Gang-won'
df.loc[df['region'] == 7, 'region'] = 'Jeju'

#gender
df.loc[df['gender'] == 1, 'gender'] = 'male'
df.loc[df['gender'] == 2, 'gender'] = 'female'

#religion
df.loc[df['religion'] == 1, 'religion'] = 'religious'
df.loc[df['religion'] == 2, 'religion'] = 'non-religious'

df.loc[df['family_member'] > 7, 'family_member'] = 7


# Calculate natural logarithm on
# 'Salary' column
df['log_income'] = np.log(df['income'])

#eliminamos algunos valores con valores inf, -inf
df=df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]

scale= StandardScaler()

df['standarized income']=scale.fit_transform(df[['income']]) 

data=df.copy()
df1=df.copy()
df1_males = df[df['gender']=='male']
df1_females = df[df['gender']=='female']
df1_males=df1_males.groupby(['year']).mean()
df1_males['year']=df1_males.index
df1_females=df1_females.groupby(['year']).mean()

df1_females['year']=df1_females.index
df2=pd.concat([df1_females, df1_males])
df1_males['income females']=df1_females['income']
df1_males['income males']=df1_males['income']
df1_males.year=df1_males.year.astype(int)
df=df[df['year']==2018]
df.reset_index(inplace=True)
df1_males['ratio females']=(df1_males['income females']/df1_males['income males']).round(2)
import streamlit as st



st.write("""
# South Korea Income 

### 2005-2018 growth & 2018 distribution

##### Xavier Martinez Bartra - Visualización de datos - Práctica 2 - UOC
    """)
    
#Fig1  
fig1 = px.bar(df1_males,x = 'year', y = ['income females','income males'],range_y=[0,10000],range_x=[2004,2019]
            ,height=400,template='ggplot2')

fig1.update_layout(paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)'
,title_text='Average income in million KRW males and females (South Korea 2005 - 2018)',
    font=dict(
        family="Century, monospace",
        color="black"
    ))

fig1.show()
st.write(fig1)


#Fig2

fig2 = px.bar(df1_males,x = 'year', y = 'ratio females',range_y=[0,1],range_x=[2004,2019],
               text="ratio females",height=400,template='ggplot2')

fig2.update_layout(paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)'
,title_text='Ratio of mean female income as a % of mean male income (South Korea 2005 - 2018)',
    font=dict(
        family="Century, monospace",
        color="black"
    ))

fig2.add_annotation(x=2008, y=0.55,
            text="50% Ratio of female income as a % of male income",
            showarrow=False,
            yshift=0)

fig2.add_shape( # add a horizontal "target" line
    type="line", line_color="black", line_width=3, opacity=0.65, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=0.5, y1=0.5, yref="y"
)

fig2.show() 
st.write(fig2)

#Fig3

df.sort_values(by='education_level',inplace=True)
fig3 = px.scatter(df,x = 'log_income', y = 'standarized income',color='gender',animation_frame='education_level',symbol='gender',
                  animation_group='education_level',text='education_level', range_y = [-1,3], range_x= [6,10],hover_name ='gender',
                  height=400,template='ggplot2')

fig3.update_traces(dict(marker_line_width=1,marker_line_color="black",mode='markers'), 
                   textposition='top center',marker_size=25)

fig3.update_layout(
    margin=dict(l=20, r=20, t=50, b=20),
    paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)'
    ,title_text='Income in mil. KRW - log and Z s. - by gender & edu. level (South Korea, 2018)',
    font=dict(
        family="Century, monospace",
        color="black"))


fig3.add_shape( # add a horizontal "target" line
    type="line", line_color="black", line_width=3, opacity=0.65, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=0, y1=0, yref="y"
)

fig3.add_annotation(x=6.8, y=0.3,
            text="Mean standarized income",
            showarrow=False,
            yshift=0)

fig3.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig3.show()
st.write(fig3)

#Fig4

df.sort_values(by='family_member',inplace=True)
fig4 = px.scatter(df,x = 'log_income', y = 'standarized income',color='gender',animation_frame='family_member',
                  symbol='gender',
                  animation_group='family_member',text='family_member', range_y = [-1,4], range_x= [6,10],
                 height=400,template='ggplot2')

fig4.update_traces(dict(marker_line_width=1,marker_line_color="black",mode='markers'),
                   textposition='top center',marker_size=25)

fig4.update_layout(
    margin=dict(l=20, r=20, t=50, b=10), 
    paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)'
,title_text='Income in mil. KRW  - log and Z s. - by gender & fam. members (South Korea, 2018)',
    font=dict(
        family="Century, monospace",
        color="black"))


fig4.add_shape( # add a horizontal "target" line
    type="line", line_color="black", line_width=3, opacity=0.65, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=0, y1=0, yref="y"
)

fig4.add_annotation(x=6.8, y=0.3,
            text="Mean standarized income",
            showarrow=False,
            yshift=0)

fig4.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig4.show()
st.write(fig4)


#Fig5

fig5=px.box(df,x="log_income",
             title="Log inc. in million KRW by region (South Korea, 2018)",template='ggplot2',color='region',
 height=400,
             color_discrete_sequence=px.colors.qualitative.Pastel).update_traces(dict(marker_line_width=1,
   marker_line_color="black")).update_traces(dict(marker_line_width=1, 
             marker_line_color="black")).update_layout( 
    paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)',
    font=dict(
        family="Century, monospace",
        color="black"))

fig5.show()
st.write(fig5)

#Fig6

fig6=px.box(df,x="log_income",
             title="Log inc. in mil. KRW religious & non religious (South Korea, 2018)",template='ggplot2',color='religion',
        height=400,
             color_discrete_sequence=px.colors.qualitative.Safe).update_traces(dict(marker_line_width=1,
   marker_line_color="black")).update_traces(dict(marker_line_width=1, 
             marker_line_color="black")).update_layout( 
    paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)',
    font=dict(
        family="Century, monospace",
        color="black"))

fig6.show()
st.write(fig6)


st.write(data.head())

st.write(""" 
### Data

 """)
st.write(""" 
https://www.kaggle.com/hongsean/korea-income-and-welfare/code

 """)






