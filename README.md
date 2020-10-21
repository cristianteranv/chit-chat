# Set up React
1. Install stuff
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save` 
  g) `pip install -U Flask-SQLAlchemy`
  h) `pip install python-dotenv`
  i) `pip install flask`

:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path that was just outputted from running which pip] install [thing you want to install]` :warning: :warning: :warning:    
2. If you already have psql set up, **SKIP THE REST OF THE STEPS AND JUST DO THE FOLLOWING COMMAND**:   
`sudo service postgresql start`    
  
# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
5. Make a new database: `sudo -u postgres createdb $USER`    
        :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for ec2-user as a user    
    c) `\l` look for ec2-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. Make an `sql.env` file that contains `DATABASE_URL='postgresql://YourUsername:YourPassword@localhost/postgres'` where you replace YourPassword and YourPassword with the value you used in 7. b)

  
# For Chuck Norris and the funtranslate API
Funtranslate does not require you to have an API key but it will limit your usage to 5 requests per hour or something along those lines, so you don't need to do anything here.
For Chuck Norris API head to rapidapi.com register for an account, look for the Chuck Norris API and replace the x-rapidapi-key inside app.py with the key you will see in your browser.
Because the Chuck Norris API is free, there shouldn't be any issue with just putting your key as a string literal inside app.py without using a .env file.
  
  
# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the DATABASE_URL with the username and password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a terminal, run python `python` from the path that contains this project's files
     In the python interactive shell, run `import models`, then `db.create_all()`, and finally `db.session.commit()`. Exit the shell with `exit()`
  b) In a new terminal, `python app.py`
  c) Preview Running Application (might have to clear your cache by doing a hard refresh)    

# Heroku
1. Sign up for heroku at heroku.com 
2. Install heroku by running `npm install -g heroku` inside your terminal.
3. Make sure that you have the DATABASE_URL variable inside your sql.env file. Go through the following steps:
    heroku login -i
    heroku create
    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:wait
    heroku pg:push pstgres DATABASE_URL
    heroku pg:psql
4. Navigate to your newly-created heroku site!
5. Configure requirements.txt with all requirements needed to run your app. (leave requirements.txt as they are right now or do pip freeze > requirements.txt in your terminal)
6. Configure Procfile with the command needed to run your app. (leave as is or just write `web: python app.py` where app.py is the name of the app unless you change it.)

# Issues during development:
Fortunately, there weren't many complex difficulties as the issues encountered were mostly due to being unfamiliar with the technologies used.
Some of the significant issues were finding a way to uniquely identify a client so that I can know who the author of a message was. The way this was fixed was by using 
socketio.request.sid (or just request.sid if you did import request from socketio). What that object? returns is a 32 character string that uniquely identifies the client that sent the message.
This client id was used as an username in this project. Whenever someone connected, I requested the sid, and sent it back to the specific client by doing 
socket.emit(channel, thingToSend, room=sid). By specifying the room as the sid you are able to send data to one specific client instead of every client.

Another thing that was a little challengin was the styling. The way I overcame this was with google lol. First, the important part for the chat was finding an element that would contain
the chat messages. Found out the most used element was a div. Furthermore, the most common element used for messages were also divs. Googling around I found some styling for messages
and found a way to give proper classes to div elements based on if the client was the one that sent the message or if it was someone else. In List.jsx, I straight up pass the className
as a prop so that I don't have to figure out which className to give inside the ListItem. Although confusing List and ListItem are not ul and li respectively
but just divs that I changed last second for better functionality with the styling I found online

Finally, another big issue I had was figuring out how SQLAlchemy works. The way I solved this was again, just googling. I gotta say that the answers to the questions I had were all very straight forward.
It was not confusing at all to understand how some methods and functions were working just by looking at the code I found online. https://flask-sqlalchemy.palletsprojects.com/en/2.x/ was a great source
that explained well what was happening with code snippets as examples. Another thing in dealing with the database was that I thought that the db.create_all() inside app.py was
sufficient to create the tables but it turned out that it wasn't. As I later found out in my class' slack chat, I had to run create_all after importing models in a python interactive shell.

#If I had more time
For known problems, I would say that a problem is that I do not know how bad or decent my code styling is at the moment. I do feel that it is not very organized and with more time
I would spend some time trying to organize it in a better way that is more reader friendly. Something that was going to go into known issues that I had enough time to fix was finding a way
to scroll the chat container to the bottom whenever a new message is sent. This was done client side whenever messages were received the code can be found in Content.jsx 
inside function getNewAddresses. Finally, a know issue is that the "sent by" for each message looks horrible right now. I want to find a way to put the username below the 
message bubble in a smaller font but did not have enough time to do it. This small font is also where the date/time the message was sent would go as well.

#Milestone 2

What are at least 2 technical issues you encountered with your project since Milestone 1?  

In this milestone I didn't run into that many issues because there weren't as many things to implement as milestone 1.
One of my technical issues difinitely was trying to figure out a way to render an image in a chat message amd making the URLs clickable. 
At first I naively tried to parse the texts on the server side using python, recognize urls, and then manipulate the text string so that the url is properly put into
a href element. However, when passing the message like that to the client side, the text printed out the html tag as part of the string instead of replacing the html tags 
with actual tags. The way I worked around this was googling solutions and running into a react component called linkify. Linkify took care of replacing every url with a
proper href tag. To handle the images, on the client side, I checked the last four characters of a text so that if an image extension is found, the text is taken and put into
the src attribute for a img element. Doing this client side apparently was enough to have the image rendered.

The next technical issue I ran into was definitely styling. I am terrible at it. I needed a way to display the profile picture inline next to the text message. 
I spent a good amount of time googling solutions and in the end ended up just trying any styling attribute I could think would be helpful. In the end I changed the 
flex orientation from column to row and that took care of that issue. However, this created another problem which was that the owner's messages (the ones that would be
on the right side of the chat container) ended up right in the middle of the container instead of sticking to the right side of the chat div. The way I fixed this was
googling again and not only searching "how do I do this" but also "trying .... is not working" and finally trying to read a little about the elements that were most relevant
to fixing this issue at w3schools. In then I fixed the error by making the message container relative and changing the margin. Setting margin-left to auto seemed to be the final
fix for my issue.


What are two ways you would improve your project if you had time?
If I had more time, I would probably look into how to make the styling better because its my biggest weakness. Additionally, I would like to be able to handle image urls
that are in the middle of text instead of only being able to handle texts that are literally just the image url. On top of that, although it feel it would be extremely complicated,
I'd like to know how to load several images in a single text message like whatsapp does. I would also have liked to implement more authorization methods but the other parts of 
the project ended up taking too much time for me to do it.