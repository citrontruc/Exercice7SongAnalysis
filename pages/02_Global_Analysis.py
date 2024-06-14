import streamlit as st

from helper.band_helper import BandExpert

st.title("Global band Analysis")

if "band_exclude" not in st.session_state:
    st.session_state["band_exclude"] = None
if "band_include" not in st.session_state:
    st.session_state["band_include"] = None
band_expert = BandExpert()

with st.sidebar:
    options_exclude = st.multiselect("Do you want to exclude some bands?", placeholder="By default, no bands are excluded", options = band_expert.get_unique_artists())
    options_include = st.multiselect("Do you want to exclude all bands except a handful?", placeholder="By default, all the bands are included", options=band_expert.get_unique_artists())
    
if options_exclude is not None:
    band_expert.set_list_exclude(options_exclude)
if options_include is not None:
    band_expert.set_list_include(options_include)

st.subheader("A few KPI about our Dataframe")
nb_band, nb_songs, oldest_song, most_recent_song = band_expert.get_dataset_kpi()
left, right = st.columns(2)
with left:
    st.markdown("**Number of bands**: " + str(nb_band))
    st.markdown("**Number of songs**: " + str(nb_songs))

with right:
    st.markdown("**Oldest song date**: " + str(oldest_song))
    st.markdown("**Most recent song date**: " + str(most_recent_song))

band_most_song = band_expert.plot_band_with_most_songs()
st.subheader("Band with most songs")
st.plotly_chart(band_most_song, theme="streamlit")

most_popular_song = band_expert.plot_most_popular_song()
st.subheader("Most popular songs")
st.plotly_chart(most_popular_song, theme="streamlit")
st.markdown("**WARNING**: Some songs don't have less than 5000 views and are excluded (too few views).")

sentiment_analysis_df = band_expert.sentiment_analysis_graph()
st.subheader("Sentiment analysis for our bands")
st.plotly_chart(sentiment_analysis_df, theme="streamlit")
st.markdown("A band is Negative if more than 70\\% of songs are negative, positive if more than 70\\% of songs are positive and neutral the rest of the time.")

year_activity = band_expert.get_plot_year_activity()
st.subheader("Repartition of song release date?")
st.plotly_chart(year_activity, theme="streamlit")
st.markdown("**WARNING**: Some songs don't have a date and are therefore excluded.")