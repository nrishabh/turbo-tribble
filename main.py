import argparse
import os
import nltk
from tqdm import tqdm
from src.data import read_metadata, read_utterances
from src.index import SearchSpaceIndex
from transformers import BertTokenizer, BertModel

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def main(args):

    assert (os.path.exists(args.data_dir)), f"Directory {args.data_dir} does not exist. It should be a folder called spotify-podcasts-2020."

    metadata = read_metadata(os.path.join(args.data_dir, 'metadata.tsv'))
    listUtterances = read_utterances(os.path.join(args.data_dir, 'podcasts-transcripts'), limit=args.data_limit)

    tokenizer = BertTokenizer.from_pretrained(args.model_name)
    model = BertModel.from_pretrained(args.model_name)

    searchspace = SearchSpaceIndex(listUtterances)
    if args.vector_mode == 'load':
        if not os.path.exists(args.vector_fp):
            raise ValueError(f"Vector file {args.vector_fp} does not exist")
        else:
            searchspace.load_vector(args.vector_fp)
    elif args.vector_mode == 'create':
        _, dir = os.path.split(args.vector_fp)
        if not os.path.exists(dir):
            os.makedirs(dir)
        for utternace in tqdm(listUtterances, desc="Vectorizing utterances", unit=' utterances'):
            utternace.vectorize(tokenizer, model)
        searchspace.create_vector(listUtterances)
        searchspace.save_vector(args.vector_fp)
    else:
        raise ValueError(f"Invalid vector mode: {args.vector_mode}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='python program to search for spotify podcasts'
    )

    parser.add_argument(
        '--data_dir',
        type=str,
        required=True,
        help='data directory (final directory should be spotify-podcasts-2020)',
        default='spotify-podcasts-2020'
    )
    parser.add_argument(
        '--model_name',
        type=str,
        required=False,
        help='transformer model name (default: bert-base-uncased))',
        default='bert-base-uncased'
    )
    parser.add_argument(
        '--vector_mode',
        type=str,
        required=True,
        help='vector mode: [create, load]',
        default='create'
    )
    parser.add_argument(
        '--data_limit',
        type=int,
        required=False,
        help='data limit (default: 100)',
        default=100
    )
    parser.add_argument(
        '--vector_fp',
        type=str,
        required=False,
        help='vector file path (to save if mode=create, to load if mode=load, default: vector.npy)',
        default='vector.npy'
    )

    args = parser.parse_args()

    main(args)
