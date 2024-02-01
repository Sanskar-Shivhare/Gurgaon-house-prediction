import streamlit as st
import pickle
import pandas as pd
import numpy as np
import lzma

st.set_page_config(page_title='Price Predictor',page_icon='🏡')


# property_type	sector	bedRoom	bathroom	balcony	agePossession	built_up_area	servant room	
# store room	furnishing_type	luxury_category	floor_category
with open('df.pkl','rb') as file:
    df = pickle.load(file)


# Specify the path to your compressed pipeline pickle file
compressed_pipeline_file_path = 'ml_pipeline_optimized_custom.pkl.xz'

# Open the compressed pipeline pickle file for reading in binary mode ('rb')
with lzma.open(compressed_pipeline_file_path, 'rb') as file:
    # Load the pipeline from the compressed pickle file
    pipeline = pickle.load(file)


st.title(':red[Price Predictor]')
st.image('predictor.png',width=300)

st.header(':blue[Enter your Inputs]')
# property_type input
property_type = st.selectbox('Property Type',['flat','house'])

# sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

# bedroom
bedroom = float(st.selectbox('Number of Bedrooms',sorted(df['bedRoom'].unique().tolist())))
# bathroom
bathroom = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

# Balcony
balcony = st.selectbox('Number of Balconies',sorted(df['balcony'].unique().tolist()))

# agePossession
property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

# buituparea
built_up_area = float(st.number_input('Built up area'))

# servant room
if st.selectbox('Servant room',['Yes','No']) == 'Yes':
    servant_room = 1.0
else:
    servant_room = 0.0

# store room
if st.selectbox('Store room',['Yes','No']) =='Yes':
    store_room = 1.
else:
    store_room = 0.


# furnishing type
furnishing_type =  st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))
    

# luxury_category
luxury_category = st.selectbox('Luxury Type',sorted(df['luxury_category'].unique().tolist()))

# floor_category
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))



if st.button('predict'):
    # make a dataframe
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'servant room', 'store room',
       'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # predict
    result = np.expm1(pipeline.predict(one_df))[0]
    low = result-0.22
    high = result+0.22

    # display

    st.text(f'The price of the {property_type} is between {np.round(low,2)} cr and {np.round(high,2)} cr')
    st.balloons()
    st.snow()


    
