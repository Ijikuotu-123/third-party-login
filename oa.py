from flask import g
import os
from flask_oauthlib.client import OAuth   #  this handles third party login

# to connect to a remote application(e.g github) ,create a OAuth object and register a  remote application(github) on it
# using the remote_app() method 
# Also, define several URLs needed for the OAuth Machinery. consumer key and secret are gotten by opening an
# account for our app on github

oauth = OAuth()     
github = oauth.remote_app( 
    'github',   # this is the name of the app it could be anything. we use github because we are dealing with it
    consumer_key= os.enivron.get('GITHUB_CONSUMER_KEY'), # get when u open an account with github(my_id)
    consumer_secret = os.environ.get('GITHUB_CONSUMER_SECRET'),  # get when u open an account with github
    request_token_param = {'scope': 'user:email'}, # request_token_param varies with the provider(facebook,twitter). this tells github will need the user email if authorized
    base_url ="https://api.github.com",  # the API url for this provider(github in this case)   
    requesr_token_url = None,    #this is none if we are using OAuth 2.0
    access_token_method = "POST",  # this is defined the method for the second request we make to the API in order to get the token
    access_token_url = "https://github.com/login/oauth/access_token", # where we send the data to so we can get the access token(takes the codes)
    authorize_url = "https://github.com/login/oauth/authorize"  # where the user will be sent to when they auhorize us(this take the state of the user)
)

@github.tokengetter          # if i don't want to do this, i will just go into github_login and put beside user
def get_github_token():      # token =g.access_token
    if 'access token' in g:
        return g.access_token

##### FOR TWITTER LOGIN ##############################################
oauth = OAuth()     
twitter = oauth.remote_app( 
    'twitter',   # this is the name of the app it could be anything. we use github because we are dealing with it
    consumer_key= os.enivron.get('TWITTER_CONSUMER_KEY'),
    consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET'),
    request_token_param = {'scope': 'user:email'}, # this depend on the client(facebook,twitter). this tells github will need the user email if authorized
    base_url ="https://api.twitter.com/1/",  # the API url for this provider(github in this case)   
    requesr_token_url = None,    #this is none if we are OAuth 2.0. for Auth1 it wont be none
    access_token_method = "POST",  # this is defined the method for the second request we make to the API in order to get the token
    access_token_url = "https://api.twitter.com/oauth/access_token", # where we send the data to so we can get the access token(takes the codes)
    authorize_url = "https://api.twitter.com/oauth/authenticate"  # where we send the user in the initial request(this take the state of the user)
)


############################################################################################################

#     USER                                           GITHUB_API                                MY_API  
# whom the client want to access data of      Host the protected user account                 That's us(client)
# 
# they authorize their client to access   
# their data from github                     verifies the account of the user when they       this is the application that
#                                             authenticate                                    wants to access the user's account
# 
#                                           issues access token to the client after the      first, user must authorize that
#                                           user  them. with the access token the client     access
#                                            can then make request to this API    
# 
#                                                                                            then, API must validate that  
#                                                                                            authorization 
# 
# 
# 
#############################################################################################################
#     
#                                             GITHUB
# 
# 
# 
# 
#          /
#         /
#        /     
#    
# 
# MY_API                        <-  Login with github(1)                                       CLIENT
#  
# (1) USER - click i want to login with github i.e i want github to give you my details for login
# (2) MY_API - sends a message to github saying give me access to this user data(e.g email). i am a real app i.e this user said you should give me his data
# MY_APP also send the it github_id  and the URI we want the user to go to if the authorize us with the message so github will know MY_APP is real
# (3) GITHUB - send a meesage to user saying authenticate yourself so we can authorize(grant access) this app.( user his present with his account or a login page if not logged in)
# the reason for this is to authenticate the user.. to be sure the user has an account with them
# (4) USER - yes i do (by choosing his account or logging in)
# (5) GITHUB - redirect the user to our REDIRECT URI that we sent with our message in step 2. it also sends a code along
# (6) MY_API - send a post request to github.the request contain the code and MY_API secret info(gotten when we register with github), so that github will know that MY_API is real
# note the user isn't involve in this stage as MY_APP secret key mustn't be known to them
# (7) GITHUB - then send to MY_API a token that indentifies the USER
# (8) MY_API - with the token can now ask GITHUB for the user's data we requested for before e.g email
#  NOTE MY_APP can only make request as long as the token hasn't expired
# 
#        

############################################
# sign_up with GITHUB
# go to settings
# go to developer settings --this leads to 3 or more tabs
# choose OAuth app and create new 0Auth app
# fill the form provided
# for the Authorization callback URL, put for now: localhost/login/github/authorized. this is where the user will be sent to
# after they authorize us
# click on submit. we will be given:
# the client_id
# the client secret

# NOTE Ensure you install Flask_Oauthlib