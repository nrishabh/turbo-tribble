
import os
import json
import csv
from collections import defaultdict

class SearchSpaceObject():

    '''
    Base class for all objects that are either indexed or searched
    '''

    def __init__(self):
        pass

    def preprocess(self, text: list, doStemming: bool = False):
        '''
        Preprocesses the text items in the object

        Args:
            text (list): list of text items
            doStemming (bool): whether to perform stemming or not

        Returns:
            list: list of preprocessed text items
        '''

        TODO:
        # 1. Convert the text to lowercase
        # 2. Remove all punctuation
        # 3. Tokenization
        # 4. Remove all stopwords
        # 5. Remove all digits
        # 6. Perform stemming (based on doStemming flag)
        pass

    def vectorize(self, text: list, engine):
        '''
        Vectorizes the text items in the object

        Args:
            text (list): list of text items
            engine (instance): vectorizer object, e.g. BERT

        Returns:
            list: list of vectorized text items
        '''

        TODO:
            # 1. Vectorize the text items using the vectorizer object
            # 2. Return the vectorized text items
        pass


class Utterance():

    '''
    Stores information about an utterance, as read from the transcript's JSON file

    Attributes:
        episode_uri: Spotify uri for the episode. e.g. spotify:episode:4vYOibPeC270jJlnRoAVO6
        text: text of the utterance
        timestamp: timestamp of the utterance
        speaker: speaker of the utterance
    '''

    episode_uri: str
    text: str
    timestamp: float
    speaker: str

    def __init__(self, text: str, timestamp: str, speaker: str):
        self.text = text
        self.timestamp = timestamp
        self.speaker = speaker


class PodcastShow(SearchSpaceObject):

    '''
    Stores information about a podcast show, as read from the TSV file

    Attributes:
        show_uri : Spotify uri for the show. e.g. spotify:show:7gozmLqbcbr6PScMjc0Zl4
        show_name : Name of the show. e.g. Reply All
        show_description : Description of the show. e.g. "’A podcast about the internet’ that is actual…”
        publisher : Publisher of the show. e.g. Gimlet
        show_filename_prefix: Filename_prefix of the show. e.g. show_7gozmLqbcbr6PScMjc0Zl4
    '''

    show_uri: str
    show_name: str
    show_description: str
    publisher: str
    show_filename_prefix: str
    listEpisodes: list

    def __init__(self, show_uri: str, show_name: str, show_description: str, publisher: str, show_filename_prefix: str):
        self.show_uri = show_uri
        self.show_name = show_name
        self.show_description = show_description
        self.publisher = publisher
        self.show_filename_prefix = show_filename_prefix
        self.listEpisodes= []

    def __str__(self):
        print(f"Show URI: {self.show_uri}")
        print(f"Show Name: {self.show_name}")
        print(f"Show Description: {self.show_description}")
        print(f"Publisher: {self.publisher}")
        return "hi"


class PodcastEpisode(SearchSpaceObject):

    '''
    Stores information about a podcast episode, as read from the TSV file

    Attributes:
        episode_uri : Spotify uri for the episode. e.g. spotify:episode:4vYOibPeC270jJlnRoAVO6
        episode_name : Name of the episode. e.g. #109 Is Facebook Spying on You?
        episode_description : Description of the episode. e.g. “This year we’ve gotten one question more than …”
        duration : duration of the episode in minutes. e.g. 31.680000
        episode_filename_prefix: Filename_prefix of the episode. e.g. 4vYOibPeC270jJlnRoAVO6
    '''

    show_uri: str
    episode_uri: str
    episode_name: str
    episode_description: str
    duration: float
    episode_filename_prefix: str
    listUtterances: list

    def __init__(self, show_uri: str, episode_uri: str, episode_name: str, episode_description: str, duration: float, episode_filename_prefix: str):
        self.show_uri = show_uri
        self.episode_uri = episode_uri
        self.episode_name = episode_name
        self.episode_description = episode_description
        self.duration = duration
        self.episode_filename_prefix = episode_filename_prefix

    def __str__(self):
        print(f"Show URI: {self.show_uri}")
        print(f"Episode URI: {self.episode_uri}")
        print(f"Episode Name: {self.episode_name}")
        print(f"Episode Description: {self.episode_description}")
        print(f"Duration: {self.duration} mins")
        return "hi"


def download_data(data_dir: str):
    '''
    Downloads the data from the dataset hosted in a Google Drive account to data_dir

    Args:
        data_dir (str): Directory where the data will be downloaded

    Returns:
        None
    '''

    # TODO:
    # 1. Download the data from the Google Drive link provided in the README.md
    # 2. Unzip the data
    # 3. Move the data to data_dir



def read_data(data_dir = "/Users/ammarpl/Downloads/info_ret/podcasts-no-audio-13GB"):

    '''
    Reads the data from data_dir and returns a list of PodcastShow and PodcastEpisode objects

    Args:
        data_dir (str): Directory where the data is downloaded

    Returns:
        listShows (list): list of PodcastsShow objects
    '''

    metadata_file = os.path.join(data_dir, 'metadata.tsv')
    shows_dict = {}
    episodes_dict = {}

    # 1. Read the data from data_dir
    # 2. Create a list of PodcastShow and PodcastEpisode objects from metadata.tsv
    with open(metadata_file, 'r', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        next(reader)  # Skip header row
        for row in reader:
            show_uri, show_name, show_description, publisher, language, rss_link, episode_uri, episode_name, episode_description, duration, show_filename_prefix, episode_filename_prefix = row

            if show_uri not in shows_dict:
                podcast_show = PodcastShow(show_uri, show_name, show_description, publisher, show_filename_prefix)
                shows_dict[show_uri] = podcast_show

            podcast_episode = PodcastEpisode(show_uri, episode_uri, episode_name, episode_description, float(duration), episode_filename_prefix)
            episodes_dict[episode_filename_prefix] = podcast_episode


    for episode_filename_prefix, episode in episodes_dict.items():
        show_dir = os.path.join(data_dir, 'spotify-podcasts-2020/podcasts-transcripts', episode.show_uri[13], episode.show_uri[14], "show_"+episode.show_uri[13:])
        json_file_path = os.path.join(show_dir, f'{episode_filename_prefix}.json')

        if not os.path.exists(json_file_path) or episode.show_uri[13]!='3' or episode.show_uri[14]!='0':
            continue
        # print("exists")
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            # 3. Create a list of Utterance objects from the JSON files
            utterances = []

            for ep in json_data['results']:
                if ep['alternatives'] and ep['alternatives'][0].get('transcript'):
                    transcript = ep['alternatives'][0]['transcript']
                    timestamp = ep['alternatives'][0]['words'][0]['startTime'][:-1]
                    speaker = ''

                    utterance = Utterance(transcript, timestamp, speaker)
                    utterances.append(utterance)
            # 4. Add the list of Utterance objects to the corresponding PodcastEpisode object
            episode.listUtterances = utterances
            shows_dict[episode.show_uri].listEpisodes.append(episode)

    # 5. Return the list of PodcastShow objects
    return list(shows_dict.values())

    # TODO:


#Example usage of read data:
listShows = read_data()
for i in range(len(listShows)):
    if listShows[i].listEpisodes != []:
        print(i)
        for j in range(len(listShows[i].listEpisodes)):
            print(listShows[i].listEpisodes[j].episode_name)
            print(listShows[i].listEpisodes[j].listUtterances[0].text)




