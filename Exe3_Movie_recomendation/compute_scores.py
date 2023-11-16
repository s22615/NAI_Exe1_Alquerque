import argparse
import numpy as np

def build_arg_parser():
    """Description of the build_arg_parser function
         Returns:
             Processed input arguments
    """
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user1', dest='user1', required=True,
                        help='First user')
    parser.add_argument('--user2', dest='user2', required=True,
                        help='Second user')
    parser.add_argument("--score-type", dest="score_type",
                        required=True,
                        choices=['Euclidean', 'Pearson'], help='Similarity metric to be used')
    return parser

def euclidean_score(dataset, user1, user2):
    """Description of the euclidean_score function
         Parameters:
         dataset: Collection of data
         user1 (string): First username given from the dataset
         user2 (string): Second username given from the dataset

         Returns:
            int: Returns Euclidean score as a float type
    """

    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    if len(common_movies) == 0:
        return 0

    squared_diff = []
    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))
            return 1 / (1 + np.sqrt(np.sum(squared_diff)))

def pearson_score(dataset, user1, user2):
    """Description of the pearson_score function
         Parameters:
         dataset: Collection of data
         user1 (string): First username given from the dataset
         user2 (string): Second username given from the dataset

         Returns:
            int: Returns Pearson score as a float type
    """

    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1
    num_ratings = len(common_movies)

    if num_ratings == 0:
        return 0
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for
                                item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for
                                item in common_movies])

    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxy == 0 or np.sqrt(Sxx * Syy) == 0:
        return 0
    else:
        return Sxy / np.sqrt(Sxx * Syy)

if __name__=='__main__':
    args = build_arg_parser().parse_args()
    user1 = args.user1
    user2 = args.user2
    score_type = args.score_type