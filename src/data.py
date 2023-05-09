
import os
import json
import string
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords


class SearchSpaceObject():

    '''
    Base class for all objects that are either indexed or searched

    Attributes:
        info_vector: vector of items that are searched or indexed with this object
    '''

    def __init__(self):
        self.info_vector = None

    def vectorize(self, text: list, tokenizer: object, model: object):
        '''
        Preprocesses the text items and returns a vectorized version of the text items

        Args:
            text (list): list of text items
            tokenizer (object): tokenizer object, e.g. transformers.Tokenizer.from_pretrained('bert-base-uncased')
            model (instance): vectorizer object, e.g. transformers.AutoModel.from_pretrained('bert-base-uncased')

        Returns:
            None
        '''
        text_items = []

        for t in text:

            # 1. Tokenization
            # t = tokenize.sent_tokenize(t)
            t = tokenizer(t, return_tensors='np')
            # 2. Convert the t to lowercase
            t = [item.lower() for item in t]
            # 3. Remove all punctuation
            t = t.translate(str.maketrans('', '', string.punctuation))
            # 4. Remove all stopwords
            t = [item for item in t if item not in stopwords.words('english')]
            # 5. Remove all digits
            t = [item for item in t if not item.isdigit()]

            text_items += t

        # 6. Vectorize the text items
        self.info_vector = model(text_items)


class Utterance():

    '''
    Stores information about an utterance, as read from the transcript's JSON file

    Attributes:
        episode_uri: Spotify uri for the episode. e.g. spotify:episode:4vYOibPeC270jJlnRoAVO6
        text: text of the utterance
        timestamp: timestamp of the utterance
    '''

    episode_uri: str
    text: str
    timestamp: float

    def __init__(self, text: str, timestamp: str):
        self.text = text
        self.timestamp = timestamp

    def vectorize(self, tokenizer: object, model: object):
        super.vectorize(self.text, tokenizer, model)


class PodcastShow(SearchSpaceObject):

    '''
    Stores information about a podcast show, as read from the TSV file

    Attributes:
        show_uri : Spotify uri for the show. e.g. spotify:show:7gozmLqbcbr6PScMjc0Zl4
        show_name : Name of the show. e.g. Reply All
        show_description : Description of the show. e.g. "’A podcast about the internet’ that is actual…”
        publisher : Publisher of the show. e.g. Gimlet
        show_filename_prefix: Filename_prefix of the show. e.g. show_7gozmLqbcbr6PScMjc0Zl4
        dictEpisodes: Dictionary of episodes in the show. Key is the episode_uri and value is the PodcastEpisode object
    '''

    show_uri: str
    show_name: str
    show_description: str
    publisher: str
    show_filename_prefix: str
    dictEpisodes: dict

    def __init__(self, show_uri: str, show_name: str, show_description: str, publisher: str, show_filename_prefix: str):
        self.show_uri = show_uri
        self.show_name = show_name
        self.show_description = show_description
        self.publisher = publisher
        self.show_filename_prefix = show_filename_prefix
        self.dictEpisodes = {}

    def __str__(self):
        return str((f"Show URI: {self.show_uri}")
                   + (f"Show Name: {self.show_name}")
                   + (f"Show Description: {self.show_description}")
                   + (f"Publisher: {self.publisher}")
                   + (f"Number of Episodes: {len(self.listEpisodes)}"))


class PodcastEpisode(SearchSpaceObject):

    '''
    Stores information about a podcast episode, as read from the TSV file

    Attributes:
        episode_uri : Spotify uri for the episode. e.g. spotify:episode:4vYOibPeC270jJlnRoAVO6
        episode_name : Name of the episode. e.g. #109 Is Facebook Spying on You?
        episode_description : Description of the episode. e.g. “This year we’ve gotten one question more than …”
        duration : duration of the episode in minutes. e.g. 31.680000
        episode_filename_prefix: Filename_prefix of the episode. e.g. 4vYOibPeC270jJlnRoAVO6
        listUtterances: List of Utterance objects
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
        self.listUtterances = []

    def __str__(self):
        return str((f"Show URI: {self.show_uri}")
                   + (f"Episode URI: {self.episode_uri}")
                   + (f"Episode Name: {self.episode_name}")
                   + (f"Episode Description: {self.episode_description}")
                   + (f"Duration: {self.duration} mins")
                   + (f"Number of Utterances: {len(self.listUtterances)}"))

    def vectorize(self, tokenizer: object, model: object):
        super.vectorize([self.episode_name, self.episode_description], tokenizer, model)


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
    pass


def read_data(data_dir: str, dev_mode: bool = False):

    '''
    Reads the data from data_dir and returns a list of PodcastShow and PodcastEpisode objects

    Args:
        data_dir (str): Directory where the data is downloaded

    Returns:
        dict: dict of PodcastsShow objects
    '''

    metadata_path = os.path.join(data_dir, 'metadata.tsv')
    transcripts_dir = os.path.join(data_dir, 'podcasts-transcripts')

    assert (os.path.exists(data_dir)), f"Directory {data_dir} does not exist. It should be a folder called spotify-podcasts-2020."
    assert (os.path.exists(metadata_path)), f"File {metadata_path} does not exist"
    assert (os.path.exists(transcripts_dir)), f"Directory {transcripts_dir} does not exist"

    metadata = pd.read_csv(metadata_path, sep='\t', header=0)

    listTranscripts = list()
    for root, dirs, files in os.walk(r"spotify-podcasts-2020\podcasts-transcripts"):
        for file in files:
            if file.endswith(".json"):
                listTranscripts.append(os.path.join(root, file))

    shows_dict = {}

    if dev_mode is True:
        listTranscripts = listTranscripts[:100]

    for transcript_path in tqdm(listTranscripts, desc="Reading transcripts", unit=" transcript"):

        transcript_dir, episode_filename_prefix = os.path.split(transcript_path)
        _, show_filename_prefix = os.path.split(transcript_dir)

        episode_filename_prefix = episode_filename_prefix[:-5]

        if show_filename_prefix in shows_dict.keys():
            show = shows_dict[show_filename_prefix]
        else:
            if metadata[metadata['show_filename_prefix'] == show_filename_prefix].empty:
                raise Exception(f"Show {show_filename_prefix} not found in metadata.tsv")
            show = PodcastShow(show_uri=metadata[metadata['show_filename_prefix'] == show_filename_prefix]['show_uri'].values[0],
                               show_name=metadata[metadata['show_filename_prefix'] == show_filename_prefix]['show_name'].values[0],
                               show_description=metadata[metadata['show_filename_prefix'] == show_filename_prefix]['show_description'].values[0],
                               publisher=metadata[metadata['show_filename_prefix'] == show_filename_prefix]['publisher'].values[0],
                               show_filename_prefix=show_filename_prefix)
            shows_dict[show_filename_prefix] = show

        if episode_filename_prefix in show.dictEpisodes.keys():
            episode = show.dictEpisodes[episode_filename_prefix]
        else:
            episode = PodcastEpisode(show_uri=metadata[metadata['episode_filename_prefix'] == episode_filename_prefix]['show_uri'].values[0],
                                     episode_uri=metadata[metadata['episode_filename_prefix'] == episode_filename_prefix]['episode_uri'].values[0],
                                     episode_name=metadata[metadata['episode_filename_prefix'] == episode_filename_prefix]['episode_name'].values[0],
                                     episode_description=metadata[metadata['episode_filename_prefix'] == episode_filename_prefix]['episode_description'].values[0],
                                     duration=metadata[metadata['episode_filename_prefix'] == episode_filename_prefix]['duration'].values[0],
                                     episode_filename_prefix=episode_filename_prefix)
            show.dictEpisodes[episode_filename_prefix] = episode

        with open(transcript_path, 'r', encoding='utf-8') as json_file:

            json_data = json.load(json_file)
            utterances = []

            for ep in json_data['results']:
                if ep['alternatives'] and ep['alternatives'][0].get('transcript'):
                    transcript = ep['alternatives'][0]['transcript']
                    timestamp = ep['alternatives'][0]['words'][0]['startTime'][:-1]
                    utterance = Utterance(transcript, timestamp)
                    utterances.append(utterance)

            episode.listUtterances = utterances

    print("Completed reading data.")
    print("Total number of shows: ", len(shows_dict.values()))
    print("Total number of episodes: ", sum([len(show.dictEpisodes.values()) for show in shows_dict.values()]))
    print("Total number of utterances: ", sum([len(episode.listUtterances) for show in shows_dict.values() for episode in show.dictEpisodes.values()]))

    return shows_dict
