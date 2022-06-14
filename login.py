from os import access
from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

Database.initialize(user="postgres",database="learning",host="localhost") 


user_email = input("Please enter your email: ")
user = User.load_from_db_by_email(user_email)


# if user exist, directly use the existed data to login Twitter.
# if user not exist, run the original pin code oauth process to construct new user data
if not user:

    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)
    
    access_token = get_access_token(request_token, oauth_verifier)

    print(access_token)

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None )
    user.save_to_db()



tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

# print(tweets)
for tweet in tweets['statuses']:
    print(tweet['text'])