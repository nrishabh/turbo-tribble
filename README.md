# Turbo Tribble
An information retrieval program for spotify podcasts that uses [open-source embeddings](https://huggingface.co/blog/getting-started-with-embeddings) to encode text into vectors and [faiss](https://github.com/facebookresearch/faiss) to perform similarity search. Inspired from the [TREC Challenge of 2020 and 2021](https://trecpodcasts.github.io/). Made for our class on [Information Retrieval and Web Agents](https://www.cs.jhu.edu/~yarowsky/cs466.html) at Johns Hopkins University during the Spring 2023 semester.

## Table of Contents
- [Turbo Tribble](#turbo-tribble)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Usage](#usage)
  - [Information](#information)
  - [Acknowledgements](#acknowledgements)

## Install
To install required libraries, run `pip install -r requirements.txt`

## Usage
```
$ python main.py -h
usage: main.py [-h] --data_dir DATA_DIR [--model_name MODEL_NAME] --vector_mode VECTOR_MODE [--vector_fp VECTOR_FP] --query_fp QUERY_FP
               [--search_mode SEARCH_MODE] [--k K] [--data_limit DATA_LIMIT]

python program to search for spotify podcasts

options:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   data directory (final directory should be spotify-podcasts-2020)
  --model_name MODEL_NAME
                        transformer model name (default: bert-base-uncased))
  --vector_mode VECTOR_MODE
                        vector mode: [create, load]
  --vector_fp VECTOR_FP
                        vector file path (to save if mode=create, to load if mode=load, default: vector.npy)
  --query_fp QUERY_FP   query file path (default: queries.xml)
  --search_mode SEARCH_MODE
                        search mode: [nndescent, hierarchical]
  --k K                 number of results to return (default: 5)
  --data_limit DATA_LIMIT
                        data limit (enter -1 for all, default: 100)
```

## Information
TODO: Link to project report (and hopefully, demo)

## Acknowledgements
Dataset was procured from Spotify's TREC Challenge of 2020 and 2021.
```
@inproceedings{clifton-etal- 2020-100000,
    title = "100,000 Podcasts: A Spoken {E}nglish Document Corpus",
    author = "Clifton, Ann  and
      Reddy, Sravana  and
      Yu, Yongze  and
      Pappu, Aasish  and
      Rezapour, Rezvaneh  and
      Bonab, Hamed  and
      Eskevich, Maria  and
      Jones, Gareth  and
      Karlgren, Jussi  and
      Carterette, Ben  and
      Jones, Rosie",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://www.aclweb.org/ anthology/2020.coling-main.519 ",
    pages = "5903--5917",
}
```

```
@misc{https://doi.org/10.48550/arxiv.2209.11871,
  doi = {10.48550/ARXIV.2209.11871},
  url = {https://arxiv.org/abs/2209.11871},
  author = {Tanaka, Edgar and Clifton, Ann and Correia, Joana and Jat, Sharmistha and Jones, Rosie and Karlgren, Jussi and Zhu, Winstead},
  keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {Cem Mil Podcasts: A Spoken Portuguese Document Corpus},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
