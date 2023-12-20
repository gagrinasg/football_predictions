import httpx
import json
import logging
import os

from app.redis_client.redis_connector import RedisConnector

class FootballAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api-football-v1.p.rapidapi.com/v3'
        self.authentication_header = "X-RapidAPI-Key"
        self.redis_connector = RedisConnector()

    async def _make_authenticated_request(self, method, path, params=None, **kwargs):
        url = f"{self.base_url}{path}"
        headers = {self.authentication_header : self.api_key}  # Modify the header name here
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, params=params, **kwargs)
            response.raise_for_status()
            return response.json()
    
    async def get_predictions_for_fixture(self, fixture_id):
        path = f"/predictions"
        params = {"fixture": fixture_id}
        response = await self._make_authenticated_request("GET", path, params=params)
        return response['response'][0]['predictions']['advice']
    
    async def get_live_fixtures(self):
        logging.info('Getting live fixtures...')
        path = f"/fixtures"
        params = {"live": 'all'}
        response = await self._make_authenticated_request("GET", path, params=params)
        fixtures_array = [fixture_details['fixture']['id'] for fixture_details in response['response']]
        return fixtures_array
    
    async def is_fixture_active(self, fixture_id: str) -> bool:
        logging.info(f'Checking if fixture id: {fixture_id} is still active')
        path = f"/fixtures"
        params = {"id": f'{fixture_id}'}
        match_finished_options = ['Match Finished', 'Match Suspended', 'Match Postponed', 'Match Cancelled','Match Abandoned']
        try:
            response = await self._make_authenticated_request(method="GET", path=path, params=params)

            if response['response'][0]['fixture']['status']['long'] in match_finished_options:
                return False
            else:
                logging.info(f'Fixture id: {fixture_id} is still active. ')
                return True
                
        except Exception as e:
            logging.error(f'Error while getting fixture details: {e}')
            return
    
    async def get_prediction_for_fixture(self, fixture_id):
        fixtures_array = await self.get_live_fixtures()

        redis = self.redis_connector.get_redis()

        # Define the key where the fixtures to be served are stored in the Redis DB
        fixtures_to_serve = "fixtures_to_serve"

        # Define the key where the fixtures that are already served are stored in the Redis DB
        fixtures_served = "fixtures_served"

        # If the set is empty, refill it with fixture IDs
        if not redis.scard(fixtures_to_serve):
            redis.sadd(fixtures_to_serve, *fixtures_array)

        # Pop a fixture ID from the set
        fixture_id = redis.spop(fixtures_to_serve)

        # Add the served fixture to the served fixture set
        redis.sadd(fixtures_served, fixture_id)

        # Convert fixture from bytes to string
        fixture_id = fixture_id.decode('utf-8')

        fixture_prediction = await self.get_predictions_for_fixture(fixture_id)
        
        return fixture_prediction
    
    async def get_live_prediction_for_ongoing_match(self):
        live_fixtures = await self.get_live_fixtures()

        redis = self.redis_connector.get_redis()

        # Define the key where the fixtures to be served are stored in the Redis DB
        fixtures_to_serve = "fixtures_to_serve"

        # Define the key where the fixtures that are already served are stored in the Redis DB
        fixtures_served = "fixtures_served"

        # If the set is empty, refill it with fixture IDs
        if not redis.scard(fixtures_to_serve):
            if len(live_fixtures) > 0:
                redis.sadd(fixtures_to_serve, *live_fixtures)
            else:
                return None, None
        
        while True:    
            # Pop a fixture ID from the set
            fixture_id = redis.spop(fixtures_to_serve)

            # Convert fixture from bytes to string
            fixture_id = fixture_id.decode('utf-8')

            # Check if fixture is still live
            if await self.is_fixture_active(fixture_id=fixture_id):
                # Add the served fixture to the served fixture set
                redis.sadd(fixtures_served, fixture_id)


                live_fixture_prediction = await self.get_predictions_for_fixture(fixture_id)
            
                return live_fixture_prediction , fixture_id
            else:
                return None, None