import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

base = 'dark'


st.set_page_config(page_title="Analytics",page_icon='📊')

st.title(":red[Analytics Module] 📈📊")
st.image('hari.png',width=300)

df = pd.read_csv('data_viz1.csv')

group_df = df.groupby('sector')[['price','price_per_sqft','built_up_area','latitude','longitude']].mean()

fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.header(':orange[map of gurgaon on the basis of area per sqft]')
st.plotly_chart(fig,use_container_width=True)



st.header(':orange[Area vs Price]')
property_type = st.selectbox('Property Type',['flat','house'])
if property_type=='flat':
    fig1 = px.scatter(df[df['property_type']=='flat'], x="built_up_area", y="price", color="bedRoom")

    st.plotly_chart(fig1)
else:
    fig1 = px.scatter(df[df['property_type']=='house'], x="built_up_area", y="price", color="bedRoom")

    st.plotly_chart(fig1)


st.header(':orange[BHK Pie chart]')
sectors = df['sector'].unique().tolist()
sectors.insert(0,'Over all')
BHKZ_type = st.selectbox('Select Sector',sectors)

if BHKZ_type=='Over all':
    fig3 = px.pie(df, names='bedRoom')
    st.plotly_chart(fig3)
else:
    fig3 = px.pie(df[df['sector']==BHKZ_type], names='bedRoom')
    st.plotly_chart(fig3)


x1 = df[df['property_type'] == 'house']['price']
x2 = df[df['property_type'] == 'flat']['price']
st.header(':orange[distribution of houses and flats]')
fig4 = ff.create_distplot([x1, x2], ['house', 'flats'], bin_size=.5,
                         curve_type='kde'
                         )

st.plotly_chart(fig4)
