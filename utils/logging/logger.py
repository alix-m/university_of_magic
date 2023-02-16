import os


def log(message):

    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '_magic_degree_tracker.log')

    with open(filename, 'a') as fp:
        fp.write('{}\n'.format(message))
