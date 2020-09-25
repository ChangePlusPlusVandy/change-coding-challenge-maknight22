# Made by michael knight as part of application for Change++ 2020 Fall
# This is a simple python script that gives the users tweets from either kanye or elon and allows them to attempt to
# guess who wrote which tweet

import random
# we will use tweepy to make it easier to interact with the twitter api
import tweepy as tw

# These are my private twitter keys that allow us access to the twitter api
consumer_key = 'g9qTWABheh04iobQf0WUJlaFo'
consumer_secret = 'vqTqg9eHN0UqCrrIwdQbnx32rEvZRv7Z0v2x1BnpRjR7IeA2Qe'
access_token = '991500266808729601-kRzQVyKzcwSkk5VGPF6ulbi11uZ7jX9'
access_secret = '6Gm2XoFQGb6GeUDoblPSO8sxV5nZbuELUj2XBWmkT60y6'

# we must set up our api access using OAuth
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# this function will allow us to filter out tweets that we do not want, such as retweets, containing links, or replies
def tweet_filter(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    elif '@' in status.full_text:
        return False
    elif 'https://' in status.full_text:
        return False
    else:
        return True


# this function will load in tweets from the specified user into a list.
def getTweets(username, holdTW):
    timeline = tw.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items()
    for status in timeline:
        if tweet_filter(status):
            data = (
                status.user.screen_name,
                status.full_text)
            holdTW.append(data)
    return holdTW


# these are the two usernames of the accounts we will be guessing with
print("Welcome to the tweet guessing game. You will be provided a tweet and you get to guess who wrote it.")
account_list = [input("Please put in the handle of the first user you would like to draw tweets from, example "
                      "'kanyewest': "),
                input("Please put in the handle of the second user you would like to draw tweets from, example "
                      "'elonmusk': ")]

twList = []  # here we will store the tweets
twList = getTweets(account_list[0], twList)  # load in kanye's tweets
twList = getTweets(account_list[1], twList)  # load in elon's tweets
print("After filtering " + str(len(twList)) + " tweets have been loaded in.")
print()

userIn = 'y'
trialsRun = 0  # how many times the game has been played
correctGuesses = 0  # how many times was the user right
while userIn == 'y' or userIn == 'Y':
    print
    ranChoice = random.choice(twList)  # select a random tweet
    trialsRun += 1  # increment the trials run
    print("Who do you think wrote the following tweet, " + account_list[0] + " or " + account_list[1] + "?")  #
    # prompt the user
    print()
    print(ranChoice[1])  # print the randomly chosen tweet
    print()
    userChoice = input(
        "Please type your answer as the users twitter handle and then press enter")  # prompt user for input
    while userChoice != account_list[0] and userChoice != account_list[
        1]:  # repeat until the user inputs a valid option
        userChoice = input('Invalid Answer: please input a valid answer')
    if userChoice == ranChoice[0]:  # if the user is correct then print this
        print('Correct! ' + ranChoice[0] + " wrote this tweet.")
        correctGuesses += 1
    else:  # if the user is wrong print this
        print('Sorry, that is wrong the correct answer was:' + ranChoice[0])
    print()
    userIn = input(
        "Would you like to play again? Press y if so, else press any key")  # ask the user if they would like to play
    # again

winningPercentage = 100 * correctGuesses / trialsRun  # what percentage of users guesses were correct
print('You got ' + str(correctGuesses) + ' out of ' + str(trialsRun) + ' guesses correct for a ' + str(
    winningPercentage) + ' win %')  # give the user their stats
print('Thanks For Playing!')
print
