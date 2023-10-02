import streamlit as st # For beautiful interface
import pandas as pd # To read the data
import plotly.express as px # To create visualizations
import pygwalker as pyg # To create your own dashboard
from streamlit_lottie import st_lottie # To display animation

st.set_page_config(layout='wide')

## load data
@st.cache_resource
def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/AshishJangra27/GFG-Hackathon/main/Hackathon%20101/medals.csv')
    data['participant_title'].fillna(data['participant_title'].mode()[0],inplace=True)
    data['country_code'].fillna(data['country_code'].mode()[0],inplace=True)
    data['athlete_url'].fillna('URL not found',inplace=True)
    data['athlete_full_name'].fillna('Anonymous',inplace=True)
    return data.sample(frac=1) ## Shuffle the dataset

#-------------------------------------------------------------------Custom Dashboard----------------------------------------------------------------------------------------

def create_your_own_tableau_db(data):
    st.title('Olympics Visualizer 🏅🏅')
    st.warning('Visualize the dataset yourself having your tableau knowledge 🚨🚨 ')
    pyg.walk(data, env='Streamlit', dark='dark')
    

#-----------------------------------------------------------Main function for a data analysis-------------------------------------------------------------------------------------
    
def main(data):
    st.title('Olympics Visualizer 🏅🏅')
    
    st.subheader('Sample data')

    ## Displaying sliced data
    edited_df = st.data_editor(data_sliced)

    ## Display the download option for the sliced data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ▶️▶️▶️▶️')
    with col2:
        st.write(' ')
    with col3:
        st.download_button(label="Download data as CSV",data=data_sliced.to_csv().encode('utf-8'),file_name='data.csv',mime='text/csv')

    slugged = data.loc[data['slug_game'] == year_of_game]
    #slugged_then_games = slugged[slugged['discipline_title'] == games]

    ## Games held at particular year and in that year, games played with medals won
    st.plotly_chart(px.bar(data.loc[data['slug_game'] == year_of_game],x='discipline_title',color='medal_type',title=f'Games held at {year_of_game}'))

    co1, co2 = st.columns(2)
    with co1:
        st.plotly_chart(px.scatter(slugged.loc[slugged['discipline_title'] == games],x='athlete_full_name',y='country_name',color='medal_type',title=f'Athletes with their Medal wons ({games})'))
    with co2:
        st.plotly_chart(px.pie(slugged,names='medal_type'))


    st.markdown(f"**🏃🏽🏃🏽{athlete_box} has won**")
    c1,c2,c3 = st.columns(3)

    medals = {'BRONZE':0,'SILVER':0,'GOLD':0}
    medals_ = dict(data.loc[data['athlete_full_name'] == athlete_box,'medal_type'].value_counts())
    if 'BRONZE' in medals_.keys():
        medals['BRONZE'] = medals_['BRONZE']
    if 'SILVER' in medals_.keys():
        medals['SILVER'] = medals_['SILVER']
    if 'GOLD' in medals_.keys():
        medals['GOLD'] = medals_['GOLD']

    with c1:
        st.write(f"{medals['BRONZE']} 🥉 **BRONZE** medal")
    with c2:
        st.write(f"{medals['SILVER']} 🥉 **SILVER** medal")
    with c3:
        st.write(f"{medals['GOLD']} 🥉 **GOLD** medal")
    
   
#----------------------------------------------------------------Loading and Sidebar Utilities--------------------------------------------------------------------------------

## call the load data function
data = load_data()
url = 'https://lottie.host/63c93f8e-f9a4-4774-b68b-a667461ddf9c/5n8ETrUGjx.json'
with st.sidebar:
    st_lottie(url,key='user')
## To set all the filters
st.sidebar.title('Filters 🥤🥤')

## Slice the data to view visualization on particular sample
slicer = st.sidebar.number_input(label='Slice the data (default - 1000) ✂️✂️',min_value=500,max_value=21697,step = 100)
data_sliced = data.head(slicer) ## Sliced data

## List of all olympic games
olympic_games = ['Curling','Freestyle Skiing','Short Track Speed Skating','Snowboard','Ski Jumping','Figure skating','Luge','Ice Hockey','Biathlon','Alpine Skiing','Skeleton','Cross Country Skiing','Speed skating','Nordic Combined','Bobsleigh','Shooting','Diving','Canoe Sprint','Cycling Road','Football','Boxing','Artistic Swimming','Handball','Rugby Sevens','Cycling BMX Racing','Triathlon','Surfing','Table Tennis','Canoe Slalom','Marathon Swimming','Trampoline Gymnastics','Volleyball','Basketball','Taekwondo','Cycling Track','Fencing','Badminton','Water Polo','Sport Climbing','Wrestling','Tennis','Artistic Gymnastics','Golf','Cycling BMX Freestyle', 'Judo','Skateboarding','Archery','Weightlifting','Baseball/Softball','Equestrian','Modern Pentathlon','Athletics','Swimming','Sailing','Cycling Mountain Bike','Rowing','Karate','3x3 Basketball','Rhythmic Gymnastics','Hockey','Beach Volleyball','Short Track','Cycling BMX','Rugby','Gymnastics Rhythmic','Equestrian Jumping','Gymnastics Artistic','Synchronized Swimming','Trampoline','Equestrian Eventing','Equestrian Dressage','Baseball','Softball','Canoe Marathon','Polo','Military Patrol', 'Tug of War','Equestrian  Vaulting','Jeu de Paume','Water Motorsports','Lacrosse','Rackets','Roque','Cricket','Croquet','Basque Pelota']
## List of athlete full name
athletes = list(data.athlete_full_name.unique())
## Years of game held
years = ['beijing-2022','tokyo-2020','pyeongchang-2018','rio-2016','sochi-2014','london-2012','vancouver-2010','beijing-2008','turin-2006','athens-2004','salt-lake-city-2002','sydney-2000','nagano-1998','atlanta-1996','lillehammer-1994','barcelona-1992','albertville-1992','seoul-1988','calgary-1988','los-angeles-1984','sarajevo-1984','moscow-1980','lake-placid-1980','montreal-1976','innsbruck-1976','munich-1972','sapporo-1972','mexico-city-1968','grenoble-1968','tokyo-1964','innsbruck-1964','rome-1960','squaw-valley-1960','melbourne-1956','cortina-d-ampezzo-1956','helsinki-1952','oslo-1952','london-1948','st-moritz-1948','berlin-1936','garmisch-partenkirchen-1936','los-angeles-1932','lake-placid-1932','amsterdam-1928','st-moritz-1928','paris-1924','chamonix-1924','antwerp-1920','stockholm-1912','london-1908','st-louis-1904','paris-1900','athens-1896']

## Select the years and view the atheltes and their medals won
year_of_game = st.sidebar.selectbox('Select the year of helding 🗓️🗓️',years)

## Select the olympic game for which you want to see the athletes and their medal won
games = st.sidebar.selectbox('Select the Olympic Game 🎲 🏏',olympic_games)

## Select the athlete and check the number of medal they won
athlete_box = st.sidebar.selectbox('Choose an ATHLETE 🏃🏼',athletes)

create = st.sidebar.checkbox('Want to create your tableau dashboard 📈📈')
if create:
    create_your_own_tableau_db(data)
else:
    main(data)





