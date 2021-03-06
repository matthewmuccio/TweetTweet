TweetTweet
==========
* A web application that implements a simple Twitter clone, built using the Flask web microframework, Bootstrap front-end framework, Jinja template engine, and SQLite RDBMS.

#### Screenshots
Feed Page (Home)
![tweettweet-feed.png](https://github.com/matthewmuccio/TweetTweet/raw/master/screenshots/tweettweet-feed.png)

Profile Page
![tweettweet-profile.png](https://github.com/matthewmuccio/TweetTweet/raw/master/screenshots/tweettweet-profile.png)

Login Page
![tweettweet-login.png](https://github.com/matthewmuccio/TweetTweet/raw/master/screenshots/tweettweet-login.png)

#### User Stories
* Users should be able to register for an account.
* Users should be able to log in.
	* Implements user session handling.
	* Implements password encryption using SHA-512.
* After logging in, users should be able to see all the posts.
* Users can make their own post that appear on a personal profile page.
* Users can click a repost button on a post that is not theirs. 

#### Planning
* PLAN OUT YOUR APPLICATION!
* Planning lowers the time it takes to develop an app. 
* What will your endpoints be?
	* What endpoint will render an HTML file?
	* What endpoint will send back JSON data?
* How might your database look like?
	* We'll have at least two models, one for users and one for posts.
	* THINK about this idea of reposting. If a user clicks a repost how will that look in the database? 
* What will your templates look like?

#### Luxury Goals
* Use Mustache.js for templating - Again, Mustache.js isn't needed but if you've tried it recently and you understand it, it can help with showing data dynamically.
* Use `hashtags` to tag keywords.
* Add a search bar that can search for those keywords.

#### Deployment
* Deploy the web application on a VPS from DigitalOcean running Ubuntu 16.04, with NGINX and firewalld.
* Check with `systemctl status firewalld` and `firewall-cmd —list-all`.
