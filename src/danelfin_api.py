from typing import List, Optional, Any
import requests

class DanelfinAPIClient:
    def __init__(self, api_key: str, api_url: str, ranking_url: str):
        self.sector_names = None
        self.api_key = api_key
        self.api_url = api_url
        self.ranking_url = ranking_url
        self.sectors_url = api_url + '/sectors'
        self.sectors: List[str] = []

    def get_all_sectors(self) -> Optional[list[Any]]:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(self.sectors_url, headers=headers)
            response.raise_for_status()
            self.sectors = response.json()
            print("Sectors retrieved successfully.")
            # from self.sectors extract the sector names
            # Extract sector names into a simple list
            self.sector_names = [item['sector'] for item in self.sectors]
            print(f"Sectors available: {self.sector_names}")

        except requests.exceptions.HTTPError as e:
            print(f"Error fetching sectors: {e}")
            return []

    def get_top5_sectors(self) -> List[str]:
        # based on average AI?
        pass

    def get_top5_industrials_from_sectors(self) -> List[str]:
        # based on average AI?
        pass

    def return_the_top_tickers(self) -> List[str]:
        pass