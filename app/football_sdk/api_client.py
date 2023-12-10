import httpx

class FootballAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api-football-v1.p.rapidapi.com/v3'
        self.authentication_header = "X-RapidAPI-Key"

    async def _make_authenticated_request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        headers = {self.authentication_header : self.api_key}  # Modify the header name here
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
    
    async def get_predictions_for_fixture(self, fixture_id):
        path = f"/predictions"
        params = {"fixture": fixture_id}
        response = await self._make_authenticated_request("GET", path, params=params)
        return response['response'][0]['predictions']['advice']
    
    async def get_live_fixtures(self):
        path = f"/fixtures"
        params = {"live": 'all'}
        response = await self._make_authenticated_request("GET", path, params=params)
        fixtures_array = [fixture_details['fixture']['id'] for fixture_details in response['response']]
        return fixtures_array
    
    async def get_prediction_for_fixture(self, fixture_id):
        fixtures_array = await self.get_live_fixtures()

        fixture_id = fixtures_array[0]

        fixture_prediction = await self.get_predictions_for_fixture(fixture_id)

        return fixture_prediction
    
    async def get_live_prediction_for_ongoing_match(self):
        live_fixtures = await self.get_live_fixtures()
        live_fixture_id = live_fixtures[0]
        live_fixture_prediction = await self.get_predictions_for_fixture(live_fixture_id)
        return live_fixture_prediction