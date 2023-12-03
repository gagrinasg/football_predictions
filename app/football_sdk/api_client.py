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
        return await self._make_authenticated_request("GET", path, params=params)