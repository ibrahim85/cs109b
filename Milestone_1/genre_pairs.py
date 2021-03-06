import ast
import operator
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

TMDB_MOVIES_COLUMN_NAMES = [
    'adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 'imdb_id',
    'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'production_companies',
    'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title',
    'video', 'vote_average', 'vote_count',
]


def load_tmdb_movies():
    df = pd.read_csv('tmdb_movies_11291.csv', header=None, names=TMDB_MOVIES_COLUMN_NAMES, encoding="utf-8")
    for column_name in ['genres', 'spoken_languages']:
        df[column_name] = df[column_name].map(lambda d: ast.literal_eval(d))
    return df


def get_fig_size(nrows=1):
    return 15, 10 * nrows


def explore_num_genres_per_movie(tmdb_movies_df):
    print 'total number of movies: %d' % len(tmdb_movies_df)

    genres_rows = tmdb_movies_df['genres']

    num_genres_per_movie_list = []
    for genres in genres_rows:
        num_genres = len(genres)
        num_genres_per_movie_list.append(num_genres)

    unique_num_genres_per_movie = set(num_genres_per_movie_list)
    print 'unique values of number of genres per movie: %s' % unique_num_genres_per_movie

    num_genres_mean = np.mean(num_genres_per_movie_list)
    print 'mean number of genres per movie: %.3f' % num_genres_mean

    _, ax = plt.subplots(1, 1, figsize=get_fig_size())
    ax.hist(num_genres_per_movie_list, bins=np.arange(-0.5, 11.0, step=1.0), alpha=0.4)
    ax.axvline(x=num_genres_mean, linewidth=2, color='k')
    plt.text(num_genres_mean + 0.1, 3700, 'num_genres mean = %.2f' % num_genres_mean)
    ax.set_xlabel('number of genres per movie')
    ax.set_ylabel('count')
    ax.set_title('Number of genres per movie')

    plt.tight_layout()
    plt.show()


def explore_genre_counts(tmdb_movies_df):
    num_movies = len(tmdb_movies_df)

    genres_rows = tmdb_movies_df['genres']
    genre_list = []
    for genres in genres_rows:
        for genre in genres:
            genre_list.append(genre['name'])

    unique_genres = set(genre_list)
    print 'number of unique genres: %d' % len(unique_genres)

    counter = Counter(genre_list)
    counter_dict = {k: float(v) / num_movies for k, v in dict(counter).items()}

    sorted_counter_items = sorted(counter_dict.items(), key=operator.itemgetter(1), reverse=True)
    for k in sorted_counter_items:
        print '%s: %.1f%%' % (k[0], k[1] * 100.0)


def get_genre_list(genres_rows):
    return [genre['name'] for genres in genres_rows for genre in genres]


def get_pair_list(genres_rows):
    pair_list = []
    for genres in genres_rows:
        for i1 in xrange(len(genres) - 1):
            g1 = genres[i1]['name']
            for i2 in xrange(i1 + 1, len(genres)):
                g2 = genres[i2]['name']
                k1 = g1 + ':' + g2
                k2 = g2 + ':' + g1
                pair_list.append(k1)
                pair_list.append(k2)
    return pair_list


def get_pair_matrix(pair_counter, sorted_genres):
    num_genres = len(sorted_genres)
    pair_matrix = np.full((num_genres, num_genres), 0, dtype=np.int)
    for i in xrange(len(sorted_genres)):
        g1 = sorted_genres[i]
        for j in xrange(i + 1, len(sorted_genres)):
            g2 = sorted_genres[j]
            count = pair_counter[g1 + ":" + g2]
            pair_matrix[i, j] = count
            pair_matrix[j, i] = count
    return pair_matrix


def get_sorted_genres(genre_list):
    genre_counter = Counter(genre_list)
    sorted_counter_items = sorted(genre_counter.items(), key=operator.itemgetter(1), reverse=True)
    sorted_genres = [i[0] for i in sorted_counter_items]
    return sorted_genres


def explore_genre_pairs(tmdb_movies_df):
    genres_rows = tmdb_movies_df['genres']
    genre_list = get_genre_list(genres_rows)
    pair_list = get_pair_list(genres_rows)

    sorted_genres = get_sorted_genres(genre_list)

    pair_counter = Counter(pair_list)

    print len(pair_list)
    print pair_counter.most_common(10)
    print pair_counter.most_common()[-10:-1]
    print len(pair_counter)

    pair_matrix = get_pair_matrix(pair_counter, sorted_genres)

    pair_df = pd.DataFrame(pair_matrix, columns=sorted_genres, index=sorted_genres)

    display(pair_df)


def calculate_conditional_probabilities(tmdb_movies_df):
    genres_rows = tmdb_movies_df['genres']
    genre_list = get_genre_list(genres_rows)
    pair_list = get_pair_list(genres_rows)

    sorted_genres = get_sorted_genres(genre_list)

    pair_counter = Counter(pair_list)
    pair_matrix = get_pair_matrix(pair_counter, sorted_genres)

    genre_counter = Counter(genre_list)
    genre_items = [num_genres for genre, num_genres in genre_counter.most_common()]
    genre_totals = np.array(genre_items)[:, np.newaxis]

    cond_probs_matrix = 100.0 * pair_matrix / genre_totals
    cond_probs_df = pd.DataFrame(cond_probs_matrix, columns=sorted_genres, index=sorted_genres)
    display(cond_probs_df.round(1))


def main():
    tmdb_movies_df = load_tmdb_movies()
    # explore_num_genres_per_movie(tmdb_movies_df)
    # explore_genre_counts(tmdb_movies_df)
    # explore_genre_pairs(tmdb_movies_df)
    calculate_conditional_probabilities(tmdb_movies_df)


if __name__ == '__main__':
    main()
