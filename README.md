# S.i.R.I. - Schoology iOS Reminders Integration
<p align="center"><img src="http://i.imgur.com/csdR86p.png?1" /></p>
A simple script that fetches your schoology events and upcoming assignments and adds them to ios reminders with a alarms and short link
## Setup
##### 🚨 I'm waiting on a PR from [here](https://github.com/picklepete/pyicloud/pull/128) to merge, which contains some necessary features. Until then you can install this using my fork as described in the setup instructions. 🚨

First things first, clone this repository to your server:

`$ git clone https://github.com/PostsDesert/SiRI.git`

Next download a fork of pyicloud...

`$ git clone https://github.com/PostsDesert/pyicloud.git`

...and install it using

`$ python3 setup.py install --user`

Now make sure you have Python 3 installed and cd in and install the dependencies, you ideally want to do this within a virtualenv if you have it installed, but otherwise you can omit those steps and just run the pip3 install line.

```
# Run this if you have virtualenv installed:
$ virtualenv .venv
$ source .venv/bin/activate
```

```
# Continue on if you have virtualenv or start here if you don't:
$ pip3 install -r requirements.txt
```
Once the requirements are installed we'll need to edit the config.py file, thats used to store our credentials and configuration options. Here's an example:

```
# Apple credentials
icloud_email = 'postsdesert@github.com'
icloud_password = 'password'

# Schoology API Key
schoology_app_key = '32hj4fhkvdieb49hnfoh4oh4'
schoology_app_secret = '38fh3ofhtoh5oghdo3hfwj49hjg94h'

# Google link Shortener API Key
goo_shorten_url_key = '3j49jgl58igjl9vjdvhd9h5493hf9ekt9h394he9tk4'

# Collection/List that you want your Schoology events to get sent to
collection = 'Schoology'
```
### How to get the keys
1. Generate an [Schoology Api Key](https://app.schoology.com/api). Copy the `consumer key` to `schoology_app_key` and `consumer secret` to `schoology_app_secret`.
2. Copy your iCloud username and password to their respective fields (`icloud_email` and `icloud_password`).
4. (optional) Generate an api key for [Google link Shortener](https://developers.google.com/url-shortener/v1/getting_started) and paste in in for `goo_shorten_url_key`.

## Set up a Crontab (optional)
1. Log into your linux account
2. Run `crontab -e`
3. paste this snipped of code on a line and save the file `30 4 * * * python3 ~/SiRI/SiRI/SiRI.py`. This will run the program at 4:30pm every day.
