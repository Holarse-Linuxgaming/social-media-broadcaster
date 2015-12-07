import requests


class GNUSocial:

    def __init__(self, url, username, password):
        self.url = url + '/api/statuses/update.xml'
        self.username = username
        self.password = password

    def make_queet(self, title, url):
        queet = title + ': ' + url

        if len(queet) > 1024:
            lenght_url = len(url)
            length_for_title = lenght_url + 7
            # 7 is for '(...): '

            queet = title[:length_for_title] + '(...): ' + url
            return queet
        else:
            return queet

    def send_queet(self, queet):
        send = requests.post(self.url, auth=(self.username, self.password),
                             data = {'status': queet})

        if send.status_code is not requests.codes.ok:
            print('Social Media Broadcaster: Error in Posting the Queet!')
            print('Social Media Broadcaster: HTML Error ' + send.status_code)
