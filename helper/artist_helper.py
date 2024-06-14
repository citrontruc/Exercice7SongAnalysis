import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import wikipedia
from wordcloud import WordCloud, STOPWORDS

class ArtistExpert():
    """
    Object to produce visualizations and KPI based on an artist.
    """
    def __init__(self):
        self.song_db = pd.read_csv("data/all_songs_df.csv", sep=";")
        self.artist_db = pd.read_csv("data/group_df.csv", sep=";")
        self.main_artist = None
    
    def set_main_artist(self, artist_name):
        """
        Sets an artist as the main artist. All the computed KPI will be about him.

        input:
            artist_name (str)
        output:
            None
        """
        self.main_artist = artist_name
    
    def get_unique_artists(self):
        """
        Produce a list of all the artists in the dataframe.

        input:
            None
        output:
            (list)
        """
        return self.song_db["band_name"].unique()
    
    def get_wikipedia_text(self):
        """
        Retrieves the wikipedia page of the main_artist.

        input:
            None
        output:
            (str)
        """
        return wikipedia.page(self.main_artist+ " (band)").summary
    
    def get_artist_kpi(self):
        """
        Retrieves some important KPI on the main_artist. (date of first song in database, date of last song in database, number of album in database, number of songs and title of the most popular song)

        input:
            None
        output:
            (date)
            (date)
            (int)
            (int)
            (str)
        """
        single_artist_db = self.artist_db.loc[self.artist_db["band_name"] == self.main_artist]
        single_song_db = self.song_db.loc[self.song_db["band_name"] == self.main_artist]
        return pd.to_datetime(single_artist_db["smallest_date"]).dt.date.iloc[0], pd.to_datetime(single_artist_db["biggest_date"]).dt.date.iloc[0], single_artist_db["num_album"].iloc[0], len(single_song_db["song_title"].unique()), single_song_db["song_title"].iloc[0]

    def plot_most_popular_songs(self):
        """
        Plots the number of views for the ten most well known songs by the main_artist.

        input:
            None
        output:
            (plotly Figure)
        """
        single_song_db = self.song_db.loc[self.song_db["band_name"] == self.main_artist].head(10)
        most_popular_song_bar = go.Figure(data=[go.Bar(x=single_song_db["song_title"], y=single_song_db["lyrics_view"], showlegend=False, text="",
                                   hovertemplate='<b>Band</b>: %{customdata[0]}<br>' +
                                      '<b>Song title</b>: %{customdata[1]}<br>' +
                                      '<b>Number of views</b>: %{customdata[2]}<br>',
                                      customdata=[(single_song_db[["band_name"]].iloc[i], single_song_db[["song_title"]].iloc[i], single_song_db[["lyrics_view"]].iloc[i]) for i in range(len(single_song_db))])])
        return most_popular_song_bar

    def plot_wordcloud(self):
        """
        Plots the wordcloud with all choruses deleted for the main_artist.

        input:
            None
        output:
            (matplotlib Figure)
        """
        single_song_db = self.song_db.loc[self.song_db["band_name"] == self.main_artist]
        single_song_db["lyrics_no_repetition"] = single_song_db["lyrics"].fillna("").apply(lambda x : "\n".join(list(set(x.split("\n")))))

        stop_words = set(list(STOPWORDS))
        song_text = " ".join(single_song_db["lyrics"].dropna().to_list())

        # Wordcloud
        wordcloud = WordCloud(width = 400, height = 400,
                    background_color ='black',
                    stopwords = stop_words,
                    min_font_size = 10,
                    collocations=False).generate(song_text)

        my_figure = plt.figure(figsize = (4, 4), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        return my_figure

    def plot_number_songs_per_year(self):
        """
        Plots the number of songs written per year for the the main_artist.

        input:
            None
        output:
            (plotly Figure)
        """
        one_band_df = self.song_db.loc[self.song_db["band_name"] == self.main_artist]
        one_band_df_with_date = one_band_df.loc[one_band_df.notna()["release_date"]]
        one_band_df_with_date["year"] = pd.to_datetime(one_band_df_with_date["release_date"]).dt.year
        year_list = one_band_df_with_date["year"].to_list()
        year_list = [int(element) for element in year_list]
        
        # Years with no songs written are absent from the dataframe.
        # We write them as 0.
        year_to_include = [i for i in range(min(year_list), max(year_list)+1)]
        num_song_per_year_list = []
        for unique_year in year_to_include:
            if unique_year in year_list:
                num_song_per_year_list.append(len(one_band_df_with_date.loc[one_band_df_with_date["year"] == unique_year]))
            else:
                num_song_per_year_list.append(0)
        number_songs_per_year = go.Figure(data=[go.Scatter(x=year_to_include, y=num_song_per_year_list, mode="lines", showlegend=True, name=self.main_artist,
                                             hovertemplate='<b>Band</b>: %{customdata[0]}<br>' +
                                      '<b>Year</b>: %{customdata[1]}<br>' +
                                      '<b>Number of songs</b>: %{customdata[2]}<br>',
                                      customdata=[(self.main_artist, year_to_include[i], num_song_per_year_list[i]) for i in range(len(year_to_include))])])
        return number_songs_per_year