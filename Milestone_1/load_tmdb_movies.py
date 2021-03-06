import ast

import pandas as pd

# reload(sys)
# sys.setdefaultencoding('utf8')

COLUMN_NAMES = [
    'adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 'imdb_id',
    'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'production_companies',
    'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title',
    'video', 'vote_average', 'vote_count',
]


def literal_conversion(d):
    return ast.literal_eval(d)


def main():
    df = pd.read_csv('tmdb_movies.csv', header=None, names=COLUMN_NAMES, nrows=11291)

    for column_name in ['genres', 'spoken_languages']:
        df[column_name] = df[column_name].map(literal_conversion)

    print df

    genres = df['genres'][0]
    print genres[0]['name']


if __name__ == '__main__':
    main()
