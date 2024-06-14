import streamlit as st

from helper.artist_helper import ArtistExpert

st.title("Artist Analysis")

if "main_artist" not in st.session_state:
    st.session_state["main_artist"] = None

artist_expert = ArtistExpert()
st.subheader("This page presents key information about an artist.")
artist_name = st.selectbox(label="Select an artist you want to know more about!", options=artist_expert.get_unique_artists(), index=None, placeholder="Write the name of an artist", key="main_artist")

if st.session_state['main_artist'] is not None:
    artist_expert.set_main_artist(artist_name)

    # Wikipedia description of the group
    wikipedia_description = artist_expert.get_wikipedia_text()
    st.subheader("Band description")
    st.markdown(wikipedia_description)

    # We write a few KPI about the group
    smallest_date, biggest_date, num_album, num_songs, most_popular_song = artist_expert.get_artist_kpi()
    st.subheader("Band KPI")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**First song Date**: " + str(smallest_date))
        st.markdown("**Last song Date**: " + str(biggest_date))
        st.markdown("**Number of Album / ep**: " + str(num_album))

    with col2:
        st.markdown("**Most popular song**: " + str(most_popular_song))
        st.markdown("**Number of songs**: "+ str(num_songs))

    # Top 10 songs with most lyrics views
    artist_top_10 = artist_expert.plot_most_popular_songs()
    st.subheader(f"Top 10 most popular songs of artist {st.session_state['main_artist']}")
    st.plotly_chart(artist_top_10, theme="streamlit")

    artist_wordcloud = artist_expert.plot_wordcloud()
    # Wordcloud to show what the group is about
    st.subheader("What is this group about?")
    st.pyplot(artist_wordcloud)
    st.markdown("**WARNING**: this wordcloud was created by removing duplicate choruses & stopwords.")
    
    # Number of songs written per year
    number_songs_per_year = artist_expert.plot_number_songs_per_year()
    st.subheader("Number of songs per year")
    st.plotly_chart(number_songs_per_year, theme="streamlit")
    st.markdown("**WARNING**: Some songs don't have a release date. We ignore them.")