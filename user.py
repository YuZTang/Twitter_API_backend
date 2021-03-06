# from database import connect
# from database import connection_pool
# from database import connection_pool2
# from database import ConnectionPool

from database import CursorFromConnectionFromPool
import oauth2
from twitter_utils import consumer
import json

class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id) -> None:
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret 
        self.id = id

    def __repr__(self) -> str:
        return f"<User {self.screen_name}>"

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)",(self.screen_name, self.oauth_token, self.oauth_token_secret))
            # cursor.execute("INSERT INTO users (email, first_name, last_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s)",(self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))
            # cursor.execute(f"INSERT INTO users (email, first_name, last_name) VALUES ({self.email}, {self.first_name}, {self.last_name})")

    @classmethod
    def load_from_db_by_screen_name(cls,screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM users WHERE screen_name = %s", (screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(screen_name=user_data[1], oauth_token = user_data[2], 
                            oauth_token_secret = user_data[3], id= user_data[0]) 

            # if user_data not exists, default return None
    

    def twitter_request(self, uri, verb='GET'):
        # Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # Make Twitter API calls
        response, content = authorized_client.request(uri, verb)

        if response.status != 200:
            print("An error occrued when searching!")
        return json.loads(content.decode('utf-8'))

    


