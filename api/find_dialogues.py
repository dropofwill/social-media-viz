import os
import tweepy

import read

##
# @returns an authenticated tweepy API instance
##
def init():
    auth = tweepy.OAuthHandler(os.environ['ROC_TWITTER_CONSUMER_KEY'],
                               os.environ['ROC_TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ROC_TWITTER_ACCESS_TOKEN'],
                          os.environ['ROC_TWITTER_ACCESS_SECRET'])
    return tweepy.API(auth)

# Create conversation graph with reply to tweets
# Lookup statuses that are outside the current DB

def main(args):
    data = read_newline_json(args.input_path, HAND_PICKED)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input-path",
            default="data/roc.liwc.json", nargs="?",
            help="path to input directory, default: 'data/roc.liwc.json'")

    main(parser.parse_args())
