
import os
import json
import torch
import string
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
from xml.dom.minidom import parse


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

            t = [item.lower() for item in t]

            t = [item.translate(str.maketrans('', '', string.punctuation)) for item in t]

            t = [item for item in t if item not in stopwords.words('english')]

            t = [item for item in t if not item.isdigit()]

            text_items += t

        tokens = tokenizer(' '.join(text_items), return_tensors='pt')
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model = model.to(device)
        self.info_vector = model(**tokens).last_hidden_state[0][0].detach().numpy()


class Query(SearchSpaceObject):

    '''
    Stores information about a query

    Attributes:
        text: text of the query
    '''

    text: str

    def __init__(self, text: str):
        self.text = text

    def vectorize(self, tokenizer: object, model: object):
        super().vectorize(self.text, tokenizer, model)


class Utterance(SearchSpaceObject):

    '''
    Stores information about an utterance, as read from the transcript's JSON file

    Attributes:
        episode_uri: Spotify uri for the episode. e.g. spotify:episode:4vYOibPeC270jJlnRoAVO6
        text: text of the utterance
        timestamp: timestamp of the utterance
    '''

    text: str
    timestamp: float
    show_filename_prefix: str
    episode_filename_prefix: str

    def __init__(self, text: str, timestamp: str, show_filename_prefix: str, episode_filename_prefix: str):
        self.text = text
        self.timestamp = timestamp
        self.show_filename_prefix = show_filename_prefix
        self.episode_filename_prefix = episode_filename_prefix

    def vectorize(self, tokenizer: object, model: object):
        super().vectorize([self.text], tokenizer, model)


def read_metadata(metadata_path: str):
    '''
    Reads the metadata from metadata_path and returns a pandas dataframe
    '''
    assert (os.path.exists(metadata_path)), f"File {metadata_path} does not exist"
    return pd.read_csv(metadata_path, sep='\t', header=0)


def read_utterances(transcripts_dir: str, limit: int = None):

    '''
    Reads the data from data_dir and returns a list of PodcastShow and PodcastEpisode objects

    Args:
        data_dir (str): Directory where the data is downloaded

    Returns:
        dict: list of Utterance objects
    '''

    assert (os.path.exists(transcripts_dir)), f"Directory {transcripts_dir} does not exist"

    listTranscriptFiles = list()
    for root, dirs, files in os.walk(transcripts_dir):
        for file in files:
            if file.endswith(".json"):
                listTranscriptFiles.append(os.path.join(root, file))

    listUtterances = []

    if limit != -1:
        print("Running in developer mode...")
        print("Limiting the number of utterances to ", limit)
        listTranscriptFiles = listTranscriptFiles[:limit]

    for transcript_path in tqdm(listTranscriptFiles, desc="Reading transcripts", unit=" transcript"):

        transcript_dir, episode_filename_prefix = os.path.split(transcript_path)
        _, show_filename_prefix = os.path.split(transcript_dir)

        episode_filename_prefix = episode_filename_prefix[:-5]

        with open(transcript_path, 'r', encoding='utf-8') as json_file:

            json_data = json.load(json_file)

            for ep in json_data['results']:
                if ep['alternatives'] and ep['alternatives'][0].get('transcript'):
                    transcript = ep['alternatives'][0]['transcript']
                    timestamp = ep['alternatives'][0]['words'][0]['startTime'][:-1]
                    utterance = Utterance(transcript, timestamp, show_filename_prefix, episode_filename_prefix)
                    listUtterances.append(utterance)

    print("Completed reading data.")
    print("Total number of utterances: ", len(listUtterances))

    return listUtterances


def read_queries(query_fp: str):

    data = parse(query_fp)

    queries = data.getElementsByTagName('description')

    results = []
    for query in queries:
        results.append(query.firstChild.data)

    return results
