import aiohttp
from typing import List, Union

from .queries import Queries
from .models import (SoundsData, Marathon, Game, Segment, Runner, Filename, Charity, Attendee, 
                     Attendance, Sound)

BOKO_API_URL = "https://bokoblin.com/api/graphql"


class AsyncBokoClient:
    """
    Asynchronus client for accessing the Bokoblin.com API
    """

    def __init__(self):
        self._session = aiohttp.ClientSession()
    
    async def _request(self, body: str, params: dict=None) -> dict:
        headers = {"Content-Type": "application/json"}
        data = {"query": body}
        if params:
            data["variables"] = params
        async with self._session.post(url=BOKO_API_URL, headers=headers, json=data) as resp:
            out = await resp.json()
            return out

    async def get_sounds_data(self) -> SoundsData:
        """
        Get the sounds data from the API
        """
        data = await self._request(Queries.SOUNDS_DATA.value)
        return SoundsData(data["data"]["soundsdata"])
    
    async def get_marathons(self) -> List[Marathon]:
        """
        Gets the full list of marathons from the API
        """
        data = await self._request(Queries.MARATHONS.value)
        return [Marathon(self._session, marathon) for marathon in data["data"]["marathons"]]
    
    async def get_marathon_by_id(self, marathon_id: int) -> Marathon:
        """
        Gets a single marathon from the API
        """
        data = await self._request(Queries.MARATHON.value, {"id": marathon_id})
        return Marathon(self._session, data["data"]["marathon"])
    
    async def get_marathon_by_name(self, marathon_name: str) -> Marathon:
        """
        Gets a single marathon from the API
        """
        marathons = await self.get_marathons()
        marathon = next((m for m in marathons if m.slug.lower() in marathon_name.lower()), None)
        if marathon is None:
            raise ValueError(f"Marathon {marathon_name} not found")
        return marathon
    
    async def get_segments_by_marathon_name(self, marathon_name: str) -> List[Segment]:
        """
        Gets all segments for a given marathon
        """
        marathon = await self.get_marathon_by_name(marathon_name)
        data = await self._request(Queries.SEGMENTS.value, {"method": "marathon", "id": int(marathon.id)})
        return [Segment(s) for s in data["data"]["segments"]]
    
    async def get_games(self) -> List[Game]:
        """
        Gets all games from the API
        """
        data = await self._request(Queries.GAMES.value)
        return [Game(game) for game in data["data"]["games"]]

    async def get_segments_by_game_name(self, game_name: str) -> List[Segment]:
        """
        Gets all segments for a given game
        """
        games = await self.get_games()
        game = next((g for g in games if g.title.lower() == game_name.lower()), None)
        if game is None:
            raise ValueError(f"Game {game_name} not found")
        data = await self._request(Queries.SEGMENTS.value, {"method": "game", "id": int(game.id)})
        return [Segment(s) for s in data["data"]["segments"]]
    
    async def get_attendees(self) -> List[Attendee]:
        """
        Gets all attendees from the API
        """
        data = await self._request(Queries.ATTENDEES.value)
        return [Attendee(attendee) for attendee in data["data"]["attendees"]]
    
    async def get_attendee_by_name(self, attendee_name: str) -> Attendee:
        """
        Gets a single attendee from the API
        """
        attendees = await self.get_attendees()
        attendee = next((a for a in attendees if a.name.lower() == attendee_name.lower()), None)
        if attendee is None:
            raise ValueError(f"Attendee {attendee_name} not found")
        return attendee
    
    async def get_runner_segments_by_name(self, runner_name: str) -> List[Segment]:
        """
        Gets all segments for a given runner
        """
        runner_id = next(r.id for r in await self.get_attendees() if r.name.lower() == runner_name.lower())
        data = await self._request(Queries.SEGMENTS.value, {"method": "runner", "id": int(runner_id)})
        return [Segment(s) for s in data["data"]["segments"]]
    
    async def get_game_by_name(self, game_name: str) -> Game:
        """
        Gets a single game from the API
        """
        games = await self.get_games()
        game = next((g for g in games if g.title.lower() == game_name.lower()), None)
        if game is None:
            raise ValueError(f"Game {game_name} not found")
        return game
    
    async def get_charities(self) -> List[Charity]:
        """
        Gets all charities from the API
        """
        data = await self._request(Queries.CHARITIES.value)
        return [Charity(self._session, data=charity) for charity in data["data"]["charities"]]

    async def get_charity_by_name(self, charity_name: str) -> Charity:
        """
        Gets a single charity from the API
        """
        charities = await self.get_charities()
        charity = next((c for c in charities if c.full_name.lower() == charity_name.lower()), None)
        if charity is None:
            raise ValueError(f"Charity {charity_name} not found")
        return charity
    
    async def get_sound(self, sound_amount: Union[int, float]) -> Sound:
        """
        Gets a single sound from the API"""
        if isinstance(sound_amount, float):
            sound_amount = sound_amount*100
        data = await self._request(Queries.SOUND.value, {"amount": sound_amount})
        if not data["data"]["sound"]:
            raise ValueError(f"No secret sound found for the specified amount!")
        return Sound(data["data"]["sound"])
    
    async def get_sounds(self) -> List[Sound]:
        """
        Get all Secret Sounds from the API
        """
        data = await self._request(Queries.SOUNDS.value)
        return [Sound(sound) for sound in data["data"]["sounds"]]
    