from pyicloud import PyiCloudService
from requests_oauthlib import OAuth1
from datetime import datetime, date
import config
import requests
import json
import os.path

class SiRI():

    def __init__(self):
        self.auth = OAuth1(config.schoology_app_key, config.schoology_app_secret, '', '')
        print("Logging in to iCloud...")
        self.icloud = PyiCloudService(config.icloud_email, config.icloud_password)
        self.update_reminders()

    # Fetch all of the user's courses
    def index_courses(self):
        print("Indexing course ids to names...")
        courses = requests.get(f'https://api.schoology.com/v1/users/{config.schoology_user_id}/sections', auth=self.auth).json()
        courses = courses['section']
        temp = {}
        for course in courses:
            temp[course['id']] = course['course_title']
        self.courses = temp


    # Fetch events from Schoology
    def fetch_schoology_events(self):
        self.index_courses()
        today = date.today().isoformat()
        events = requests.get(f'https://api.schoology.com/v1/users/{config.schoology_user_id}/events?start_date={today}', auth=self.auth).json()
        events = events['event']
        temp = []
        for event in events:
            try:
                temp.append({
                    "title":            event['title'],
                    "description":      event['description'],
                    "course_id":        event['section_id'],
                    "assignment_id":    event['assignment_id'],
                    "date":             event['start'],
                    "all_day":          event['all_day']
                })
            except KeyError:
                continue
        self.events = temp

    # Shorten links for events
    def goo_shorten_url(self, assignment_id):
        url = f'https://app.schoology.com/assignment/{assignment_id}'
        if config.goo_shorten_url_key == "":
            return url
        post_url = f'https://www.googleapis.com/urlshortener/v1/url?key={config.goo_shorten_url_key}'
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        return r.json()['id']

    def add_reminder(self, event):
        course_name = self.courses[str(event['course_id'])]
        title = f"{event['title']} : {course_name}"
        description = self.goo_shorten_url(event['assignment_id'])
        date = event['date']  # 2017-04-18 15:15:00 0123-56-78 12:45:78
        collection = config.collection
        print('sending...')
        print(event)
        self.icloud.reminders.post(title=title, description=description, collection=collection, dueDate=datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16])))
        print('sent.')

    def send_reminders(self, events):
        duplicates = 0
        total = 0
        print("Sending events to Reminders...")
        for event in self.events:
            for reminder in self.reminders_to_add:
                if event['title'] in reminder:
                    duplicates += 1
                    break
            else:
                self.add_reminder(event)
                total += 1
        print(f"Completed. {duplicates} duplicates found. {total} events sent to Reminders")

    def get_current_reminders(self):
        print('Getting current reminders...')
        reminders = self.icloud.reminders.refresh()[config.collection]
        current_reminders = []
        for reminder in reminders:
            current_reminders.append(reminder['title'])
        scriptpath = os.path.dirname(__file__)
        dataFile = os.path.join(scriptpath, 'data.json')
        try:
            with open(dataFile) as json_file:
                existing_reminders = json.load(json_file)
        except:
            print('Creating data.json...')
            existing_reminders = []
            with open(dataFile, 'w') as outfile:
                json.dump(existing_reminders, outfile)
        future_events = []
        for event in self.events:
            future_events.append(event['title'])

        self.reminders_to_add = current_reminders + list(set(existing_reminders) - set(current_reminders))
        self.all_reminders = self.reminders_to_add + list(set(future_events) - set(self.reminders_to_add))
        try:
            with open(dataFile, 'w') as outfile:
                json.dump(self.all_reminders, outfile)
        except:
            print("Could not write to data.json")

        return self.reminders_to_add

    def update_reminders(self):
        self.fetch_schoology_events()
        self.get_current_reminders()
        self.send_reminders(self.events)

if __name__ == "__main__":
    SiRI()
