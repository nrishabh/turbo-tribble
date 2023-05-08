class SearchSpaceObject():

    '''
    Base class for all classes that have text items that need to be searched for
    '''

    def __init__(self):
        pass

    def preprocess(self, text: list):
        '''
        Preprocesses the text items in the object

        Args:
            text (list): list of text items

        Returns:
            list: list of preprocessed text items
        '''
        pass

    def vectorize(self, text: list):
        '''
        Vectorizes the text items in the object

        Args:
            text (list): list of text items

        Returns:
            list: list of vectorized text items
        '''
        pass


class Utterance(SearchSpaceObject):

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

    def __str__(self):
        print(f"Show URI: {self.show_uri}")
        print(f"Show Name: {self.show_name}")
        print(f"Show Description: {self.show_description}")
        print(f"Publisher: {self.publisher}")


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


def read_data(data_dir):

    '''
    Reads the data from data_dir and returns a list of PodcastShow and PodcastEpisode objects

    Args:
        data_dir (str): Directory where the data is downloaded

    Returns:
        listShows (list): list of PodcastsShow objects
    '''

    # TODO:
    # 1. Read the data from data_dir
    # 2. Create a list of PodcastShow and PodcastEpisode objects from metadata.tsv
    # 3. Create a list of Utterance objects from the JSON files
    # 4. Add the list of Utterance objects to the corresponding PodcastEpisode object
    # 5. Return the list of PodcastShow objects