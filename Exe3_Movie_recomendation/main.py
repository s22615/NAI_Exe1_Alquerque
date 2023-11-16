import argparse
import json
import numpy as np
from compute_scores import pearson_score

"""
Author
    Sebastian Mackiewicz - PJAIT student

Build movie recommendation engine that returns 5 movies that should interest given user and he didn't watched that yet. 
After that returns 5 movies that given user should not watch it.

Before running program install
pip install numpy

Make sure you have installed python at least in version 3.10

After that in terminal, cmd or PowerShell type 
$ python main.py --user "HERE ENTER USERNAME"
"""
def build_arg_parser():
    """Description of the build_arg_parser function
         Returns:
             Processed input arguments
    """
    parser = argparse.ArgumentParser(description='Find recommendations for the given user')
    parser.add_argument('--user', dest='user', required=True, help='Input user')
    return parser

def get_recommendations(dataset, input_user):
    """Description of the get_recommendations function
        Parameters:
             dataset: Collection of data
             input_user: Name of user that data is searched for
        Returns:
             List: Return list of movie_recommendations
    """

    if input_user not in dataset:
        raise TypeError('Cannot find ' + input_user + ' in the dataset')

    overall_scores = {}
    similarity_scores = {}

    for user in [x for x in dataset if x != input_user]:
        similarity_score = pearson_score(dataset, input_user, user)
        if similarity_score <= 0:
            continue

        filtered_list = [x for x in dataset[user] if x not in dataset[input_user] or dataset[input_user][x] == 0]

        for item in filtered_list:
            if item in overall_scores:
                overall_scores[item] += dataset[user][item] * similarity_score
            else:
                overall_scores[item] = dataset[user][item] * similarity_score

            if item in similarity_scores:
                similarity_scores[item] += similarity_score
            else:
                similarity_scores[item] = similarity_score

    if len(overall_scores) == 0:
        return ['No recommendations possible']

    movie_scores = np.array([[score / similarity_scores[item], item]
                             for item, score in overall_scores.items()])

    movie_scores = movie_scores[np.argsort(movie_scores[:, 0])[::-1]]

    movie_recommendations = [movie for _, movie in movie_scores]
    return movie_recommendations

if __name__=='__main__':
    args = build_arg_parser().parse_args()
    user = args.user

    with open('raitings.json', 'r') as f:
        data = json.loads(f.read())

    print("Movie recommended for " + user + ":")
    movies = get_recommendations(data, user)

    for i, movie in enumerate(movies[:5]):
        print('- ' + movie)
    print("")
    print("Movie not recommended for " + user + ":")
    for i, movie in enumerate(movies[-5:]):
        print('- ' + movie)
