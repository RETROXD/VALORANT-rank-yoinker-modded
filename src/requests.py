import base64
from distutils import errors
import json
import time

import requests
from colr import color
import os


class Requests:
    def __init__(self, version, log, Error):
        self.Error = Error
        self.version = version
        self.headers = {}
        self.log = log

        self.region = self.get_region()
        self.pd_url = f"https://pd.{self.region[0]}.a.pvp.net"
        self.glz_url = f"https://glz-{self.region[1][0]}.{self.region[1][1]}.a.pvp.net"
        self.log(f"Api urls: pd_url: '{self.pd_url}', glz_url: '{self.glz_url}'")
        self.region = self.region[0]
        self.lockfile = self.get_lockfile()

        self.puuid = ''
        #fetch puuid so its avaible outsite
        self.get_headers()

    def check_version(self):
        # checking for latest release
        r = requests.get("https://api.github.com/repos/isaacKenyon/VALORANT-rank-yoinker/releases")
        json_data = r.json()
        release_version = json_data[0]["tag_name"]  # get release version
        link = json_data[0]["assets"][0]["browser_download_url"]  # link for the latest release

        if float(release_version) > float(self.version):
            print(f"New version available! {link}")


    def check_status(self):
        # checking status
        rStatus = requests.get(
            "https://raw.githubusercontent.com/isaacKenyon/VALORANT-rank-yoinker/main/status.json").json()
        if not rStatus["status_good"] or rStatus["print_message"]:
            status_color = (255, 0, 0) if not rStatus["status_good"] else (0, 255, 0)
            print(color(rStatus["message_to_display"], fore=status_color))
            
    def fetch(self, url_type: str, endpoint: str, method: str):
        try:
            if url_type == "glz":
                response = requests.request(method, self.glz_url + endpoint, headers=self.get_headers(), verify=False)
                self.log(f"fetch: url: '{url_type}', endpoint: {endpoint}, method: {method},"
                    f" response code: {response.status_code}")
                if not response.ok:
                    time.sleep(5)
                    self.headers = {}
                    self.fetch(url_type, endpoint, method)
                return response.json()
            elif url_type == "pd":
                response = requests.request(method, self.pd_url + endpoint, headers=self.get_headers(), verify=False)
                self.log(
                    f"fetch: url: '{url_type}', endpoint: {endpoint}, method: {method},"
                    f" response code: {response.status_code}")
                if not response.ok:
                    time.sleep(5)
                    self.headers = {}
                    self.fetch(url_type, endpoint, method)
                return response
            elif url_type == "local":
                local_headers = {'Authorization': 'Basic ' + base64.b64encode(
                    ('riot:' + self.lockfile['password']).encode()).decode()}
                response = requests.request(method, f"https://127.0.0.1:{self.lockfile['port']}{endpoint}",
                                            headers=local_headers,
                                            verify=False)
                if endpoint != "/chat/v4/presences":
                    self.log(
                        f"fetch: url: '{url_type}', endpoint: {endpoint}, method: {method},"
                        f" response code: {response.status_code}")
                return response.json()
            elif url_type == "custom":
                response = requests.request(method, f"{endpoint}", headers=self.get_headers(), verify=False)
                self.log(
                    f"fetch: url: '{url_type}', endpoint: {endpoint}, method: {method},"
                    f" response code: {response.status_code}")
                if not response.ok: self.headers = {}
                return response.json()
        except json.decoder.JSONDecodeError:
            self.log(f"JSONDecodeError in fetch function, resp.code: {response.status_code}, resp_text: '{response.text}")
            print(response)
            print(response.text)

    def get_region(self):
        path = os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log')
        with open(path, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if '.a.pvp.net/account-xp/v1/' in line:
                    pd_url = line.split('.a.pvp.net/account-xp/v1/')[0].split('.')[-1]
                elif 'https://glz' in line:
                    glz_url = [(line.split('https://glz-')[1].split(".")[0]),
                               (line.split('https://glz-')[1].split(".")[1])]
                if "pd_url" in locals().keys() and "glz_url" in locals().keys():
                    self.log(f"got region from logs '{[pd_url, glz_url]}'")
                    return [pd_url, glz_url]

    def get_current_version(self):
        path = os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log')
        with open(path, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if 'CI server version:' in line:
                    version_without_shipping = line.split('CI server version: ')[1].strip()
                    version = version_without_shipping.split("-")
                    version.insert(2, "shipping")
                    version = "-".join(version)
                    self.log(f"got version from logs '{version}'")
                    return version

    def get_lockfile(self):
        path = os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')
        
        if self.Error.LockfileError(path):
            with open(path) as lockfile:
                self.log("opened lockfile")
                data = lockfile.read().split(':')
                keys = ['name', 'PID', 'port', 'password', 'protocol']
                return dict(zip(keys, data))


    def get_headers(self):
        if self.headers == {}:
            local_headers = {'Authorization': 'Basic ' + base64.b64encode(
                ('riot:' + self.lockfile['password']).encode()).decode()}
            response = requests.get(f"https://127.0.0.1:{self.lockfile['port']}/entitlements/v1/token",
                                    headers=local_headers, verify=False)
            entitlements = response.json()
            self.puuid = entitlements['subject']
            headers = {
                'Authorization': f"Bearer {entitlements['accessToken']}",
                'X-Riot-Entitlements-JWT': entitlements['token'],
                'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjog"
                                         "IldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5"
                                         "MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
                'X-Riot-ClientVersion': self.get_current_version(),
                "User-Agent": "ShooterGame/13 Windows/10.0.19043.1.256.64bit"
            }
        return headers

    def get_ranked_history(self, puuid):
        try:
            rMatches = requests.request("GET", f"https://pd.{self.region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates?queue=competitive", headers=self.get_headers(), verify=False).json()
            self.log(f"REQUEST: Got ranked history for {puuid}")
            last_5_matches = []
            last_5_match_ids = []
            if rMatches['Matches'] == []:
                last_5_matches = [0, 0, 0, 0, 0]
                last_5_match_ids = ["", "", "", "", ""]

            if len(rMatches['Matches']) >= 5:
                for i in range(5):
                    if rMatches["Matches"][i]["RankedRatingEarned"] is not None:
                        last_5_matches.append(rMatches["Matches"][i]["RankedRatingEarned"])
                        last_5_match_ids.append(rMatches["Matches"][i]["MatchID"])
                self.log(f"REQUEST: Retrieved last 5 matches: {last_5_matches}")
            
            elif len(rMatches['Matches']) < 5 and len(rMatches['Matches']) > 0:
                for i in range(len(rMatches['Matches'])):
                    if rMatches["Matches"][i]["RankedRatingEarned"] is not None:
                        last_5_matches.append(rMatches["Matches"][i]["RankedRatingEarned"])
                        last_5_match_ids.append(rMatches["Matches"][i]["MatchID"])
                self.log(f"REQUEST: Retrieved last 5 matches: {last_5_matches}")
            else:
                last_5_matches = [0, 0, 0, 0, 0]
                last_5_match_ids = ["", "", "", "", ""]
            
            return [last_5_matches, last_5_match_ids]
        except json.decoder.JSONDecodeError:
            self.log("ERROR :: REQUEST: JSONDecodeError in get_ranked_history function, likely rate limit exceeded")
            return [[0, 0, 0, 0, 0], ["", "", "", "", ""]]

    def get_match_details(self, match_id):
        try:
            match_details = requests.request("GET", f"https://pd.{self.region}.a.pvp.net/match-details/v1/matches/{match_id}", headers=self.get_headers(), verify=False).json()
            self.log(f"REQUEST: Got match details for {match_id}")
            if 'httpStatus' in match_details:
                return ["nomatches"]
            return match_details
        except json.decoder.JSONDecodeError:
            self.log("ERROR :: REQUEST: JSONDecodeError in get_match_details function, likely rate limit exceeded")
            return ["nomatches"]

    def get_kda(self, puuid, match_ids):
        try:
            matches = match_ids
            self.log(f"REQUEST: Got recent matches for {puuid}")
            if matches == ["", "", "", "", ""]:
                return [
                    [1], 
                    [1], 
                    [1]
                    ]
            else:
                # create kda list to store kda values
                kills = []
                deaths = []
                assists = []
                counter = 0
                
                for match in matches:
                    if counter == 1:
                        break
                    match_details = Requests.get_match_details(self, match)
                    self.log(f"REQUEST: Got match details for {match}")
                    if match_details == ["nomatches"]:
                        continue
                    else:
                        for match in match_details['players']:
                            if match['subject'] != puuid:
                                continue
                            kills.append(match['stats']['kills'])
                            deaths.append(match['stats']['deaths'])
                            assists.append(match['stats']['assists'])
                            counter += 1
                self.log(f"REQUEST: Got KDA for {puuid} :: {kills} :: {deaths} :: {assists}")
                return [kills, deaths, assists]
        except json.decoder.JSONDecodeError:
            self.log("ERROR :: REQUEST: JSONDecodeError in get_kda function, likely rate limit exceeded")
            return [
                    [1], 
                    [1], 
                    [1]
                    ]