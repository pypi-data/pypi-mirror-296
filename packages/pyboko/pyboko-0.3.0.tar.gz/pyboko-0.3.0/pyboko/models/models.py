from dateutil.parser import isoparse
from typing import List

from .enums import AttendeeRank, RunnerRank


BOKO_API_URL = "https://bokoblin.com/api/graphql"


class Marathon:
    def __init__(self, session, data):
        self._session = session
        self.id = int(data.get("id", None))
        self.type = data.get("type", None)
        self.type_id = data.get("type_id", None)
        self.slug = data.get("slug", None)
        self.full_name = data.get("full_name", None)
        self.total = data.get("total", None)
        self.donations_over_time = data.get("donationsTime", None)
        sd = data.get("start_date", None)
        if sd:
            self.start_date = isoparse(sd)
        else:
            self.start_date = sd
        ed = data.get("stop_date", None)
        if ed:
            self.stop_date = isoparse(ed)
        else:
            self.stop_date = ed
        self.playlist = data.get("playlist", None)
        self.charity = Charity(None, data.get("charity", None)) if data.get("charity", None) else None
        self.segments = [Segment(segment) for segment in data.get("segments", [])]
        self.attendance = [Attendance(attendee) for attendee in data.get("attendance", [])]
        self.color = data.get("color", None)
    
    async def get_attendees(self):
        """
        Gets a list of attendees for the marathon
        """
        body = """
        query($marathon_id: Int!){
            marathon(id: $marathon_id){
                attendance{
                    location
                    attendee{
                        id
                        name
                        twitch_login
                        rank
                        house
                        house_color
                    }
                    award
                }
            }
        }"""
        headers = {"Content-Type": "application/json"}
        async with self._session.post(url=BOKO_API_URL, headers=headers, json={"query": body, "variables": {"marathon_id": int(self.id)}}) as resp:
            data = await resp.json()
        self.attendance = [Attendance(attendee) for attendee in data["data"]["marathon"]["attendance"]]

    async def get_segments(self):
        """
        Gets a list of segments that occurred during the marathon
        """
        body = """
        query($marathon_id: Int!){
            marathon(id: $marathon_id){
                segments{
                    id
                    game{
                        id
                        title
                        isZelda
                        isEvent
                    }
                    modifier
                    raised
                    start_time
                    end_time
                    vod
                    time_offset
                    runners{
                        attendee{
                            id
                            name
                            twitch_login
                            rank
                        }
                        rank
                    }
                    filenames{
                        filename
                        note
                    }
                }
            }
        }"""
        headers = {"Content-Type": "application/json"}
        async with self._session.post(url=BOKO_API_URL, headers=headers, json={"query": body, "variables": {"marathon_id": int(self.id)}}) as resp:
            data = await resp.json()
        self.segments = [Segment(segment) for segment in data["data"]["marathon"]["segments"]]

    def __str__(self):
        return f"<Marathon {self.full_name} (number {self.id}): raised {self.total} for {self.charity.full_name}>"
    
    def __repr__(self):
        return self.__str__()


class Segment:
    def __init__(self, data):
        self.id = data.get("id", None)
        mar = data.get("marathon", None)
        if mar:
            self.marathon = Marathon(mar)
        else:
            self.marathon = None
        self.game = Game(data.get("game", None))
        self.modifier = data.get("modifier", None)
        self.raised = data.get("raised", None)
        sd = data.get("start_time", None)
        if sd:
            self.start_time = isoparse(sd)
        else:
            self.start_time = sd
        ed = data.get("end_time", None)
        if ed:
            self.end_time = isoparse(ed)
        else:
            self.end_time = ed
        self.vod = data.get("vod", None)
        self.time_offset = data.get("time_offset", None)
        self.runners = [Runner(runner) for runner in data.get("runners")]
        self.filenames = [Filename(filename) for filename in data.get("filenames")]


class Runner:
    def __init__(self, data):
        self.attendee = Attendee(data.get("attendee", None))
        self.rank = RunnerRank.from_rank_num(data.get("rank", None))


class Filename:
    def __init__(self, data):
        self.segment_id = data.get("segment_id", None)
        self.filename = data.get("filename", None)
        self.note = data.get("note", None)


class Game:
    def __init__(self, data):
        self.id = data.get("id", None)
        self.title = data.get("title", None)
        self.segments = [Segment(segment) for segment in data.get("segments", [])]
        self.isZelda = data.get("isZelda", None)
        self.isEvent = data.get("isEvent", None)


class Charity:
    def __init__(self, _session, data):
        self.id = data.get("id", None)
        self.slug = data.get("slug", None)
        self.full_name = data.get("full_name", None)
        self.website = data.get("website", None)
        self.total = float(data.get("total", None))
        self.marathons = [Marathon(_session, marathon) for marathon in data.get("marathons", [])]


class Attendance:
    def __init__(self, data):
        self.id = data.get("id", None)
        att = data.get("attendee", None)
        if att:
            self.attendee = Attendee(att)
        else:
            self.attendee = None
        mar = data.get("marathon", None)
        if mar:
            self.marathon = Marathon(mar)
        else:
            self.marathon = None

        self.award = data.get("award", None)
        self.location = data.get("location", None)


class Attendee:
    def __init__(self, data):
        self.id = data.get("id", None)
        self.name = data.get("name", None)
        self.twitch_login = data.get("twitch_login", None)
        self.rank = AttendeeRank.from_rank_num(data.get("rank", None))
        self.house = data.get("house", None)
        self.house_color = data.get("house_color", None)
