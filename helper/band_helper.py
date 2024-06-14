from colorsys import hls_to_rgb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

class BandExpert():
    def __init__(self):
        self.song_db = pd.read_csv("data/all_songs_df.csv", sep=";")
        self.artist_db = pd.read_csv("data/group_df.csv", sep=";")
        self.song_db["release_date"] = pd.to_datetime(self.song_db["release_date"])
        self.colourmap = self.generate_colourmap()
        self.artist_db["colour"] = self.artist_db["band_name"].map(self.colourmap).apply(lambda x : '#%02x%02x%02x' % (int(x[0]), int(x[1]), int(x[2])))
        self.song_db["colour"] = self.song_db["band_name"].map(self.colourmap).apply(lambda x : '#%02x%02x%02x' % (int(x[0]), int(x[1]), int(x[2])))
        self.list_exclude = None
        self.list_include = None
    
    def set_list_include(self, list_include):
        self.list_include = list_include
    
    def set_list_exclude(self, list_exclude):
        self.list_exclude = list_exclude
    
    def filter_df(self, db_filter):
        if self.list_exclude:
            db_filter = db_filter.loc[~db_filter["band_name"].isin(self.list_exclude)]
        if self.list_include:
            db_filter = db_filter.loc[db_filter["band_name"].isin(self.list_include)]
        return db_filter
    
    def get_unique_artists(self):
        """
        Produce a list of all the artists in the dataframe.

        input:
            None
        output:
            (list)
        """
        return self.song_db["band_name"].unique()

    def generate_colourmap(self):
        """
        Generates a colourmap with an unique colour for each of the values in the column interest_column

        Input:
            Pandas_df (pandas dataframe): the dataframe with the values
            interest_column (str): column on which to filter
        
        Output:
            (dict)
        """
        interest_list = self.get_unique_artists()
        colourscale_hls = sns.color_palette("husl", len(interest_list))
        colourscale = []
        for element in colourscale_hls:
            colourscale.append(tuple([value * 255 for value in hls_to_rgb(*element)]))
        colourmap = {col_val : colour for col_val, colour in zip(interest_list, colourscale)}
        return colourmap

    def get_dataset_kpi(self):
        # Nb bands, nb total chansons, vulgarité...
        filter_song = self.filter_df(self.song_db)
        nb_band = len(filter_song["band_name"].unique())
        nb_songs = len(filter_song)
        oldest_song = filter_song["release_date"].dropna().dt.date.min()
        most_recent_song = filter_song["release_date"].dropna().dt.date.max()
        return nb_band, nb_songs, oldest_song, most_recent_song

    def plot_band_with_most_songs(self):
        inter_db = self.filter_df(self.artist_db)
        song_count = inter_db.sort_values("song_title", ascending=False).head(10)[["band_name", "song_title", "colour"]]
        song_count_bar = go.Figure([go.Bar(x=song_count["band_name"], y=song_count["song_title"], marker={"color" : song_count["colour"]}, showlegend=False, text=song_count["song_title"],
                            hovertemplate='<b>Band</b>: %{customdata[0]}<br>' +
                                      '<b>Number of songs written</b>: %{customdata[1]}<br>',
                                      customdata=[(song_count[["band_name"]].iloc[i], song_count[["song_title"]].iloc[i]) for i in range(len(song_count))])])
        return song_count_bar

    def sentiment_analysis_graph(self):
        # We need to get the number of songs per artist
        num_song_per_artist = self.song_db.groupby("band_name")["lyrics"].count().reset_index()
        num_positive_artist = (self.artist_db["POSITIVE"] > num_song_per_artist["lyrics"]*0.7).sum()
        num_negative_artist = (self.artist_db["NEGATIVE"] > num_song_per_artist["lyrics"]*0.7).sum()
        num_neutral_artist = len(self.artist_db) - num_positive_artist - num_negative_artist
        positivity_graph = go.Figure([go.Bar(x=["NEGATIVE", "NEUTRAL", "POSITIVE"], y=[num_negative_artist, num_neutral_artist, num_positive_artist], text=[num_negative_artist, num_neutral_artist, num_positive_artist])])
        return positivity_graph

    def plot_most_popular_song(self):
        inter_db = self.filter_df(self.song_db)
        song_count = inter_db.sort_values("lyrics_view", ascending=False).head(10)[["band_name", "song_title", "lyrics_view", "colour"]]
        song_count_bar = go.Figure([go.Bar(x=song_count["song_title"], y=song_count["lyrics_view"], marker={"color" : song_count["colour"]}, showlegend=False, text="",
                            hovertemplate='<b>Band</b>: %{customdata[0]}<br>' +
                                      '<b>Song title</b>: %{customdata[1]}<br>' +
                                      '<b>Number of views</b>: %{customdata[2]}<br>',
                                      customdata=[(song_count[["band_name"]].iloc[i], song_count[["song_title"]].iloc[i], song_count[["lyrics_view"]].iloc[i]) for i in range(len(song_count))])])
        return song_count_bar

    def get_plot_year_activity(self):
        inter_db = self.filter_df(self.song_db)
        inter_db["release_date"] = pd.to_datetime(inter_db["release_date"]).dt.date
        fig = px.box(inter_db, x="release_date")
        return fig