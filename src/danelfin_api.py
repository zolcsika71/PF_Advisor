from typing import List, Optional, Any
import requests

class DanelfinAPIClient:
    def __init__(self, date: str, api_key: str, api_url: str, ranking_url: str):
        self.cache = {}
        self.sector_names = None
        self.date = date
        self.header = {"Authorization": f"Bearer {api_key}"}
        self.api_url = api_url
        self.ranking_url = ranking_url
        self.sectors_url = api_url + '/sectors'
        self.sectors: List[str] = []

    def get_all_sectors(self) -> Optional[list[Any]]:
        try:

            response = requests.get(self.sectors_url, headers=self.header)
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
        """
        Get the top 5 sectors based on both:
        1. Number of high AI score stocks
        2. Average sector performance
        
        The date parameter is used from the instance variable.
        
        Returns:
            List of the top 5 sector names
        """
        # Make sure we have the sector names
        if not self.sector_names:
            self.get_all_sectors()
            
        if not self.sector_names:
            print("Error: Unable to retrieve sectors")
            return []
            
        # Check if we have a cache
        if not hasattr(self, 'cache'):
            self.cache = {}
            
        # Define a cache key using the current date
        cache_key = f"top5_sectors_{self.date}"
        if cache_key in self.cache:
            print(f"Using cached result for {cache_key}")
            return self.cache[cache_key]
        

        
        # Track sector metrics in a dictionary
        sectors_data = {}
        
        try:
            # First, get all stocks in all sectors for the date
            response = requests.get(self.ranking_url, params=self.date, headers=self.header)
            response.raise_for_status()
            all_stocks = response.json()
            
            # Process the data by sector
            for date_key, tickers in all_stocks.items():
                # We only need to process the first date entry
                for ticker, ticker_data in tickers.items():
                    if "sector" in ticker_data and "aiscore" in ticker_data:
                        sector = ticker_data["sector"]
                        ai_score = int(ticker_data["aiscore"])
                        
                        # Initialize sector data if not already present
                        if sector not in sectors_data:
                            sectors_data[sector] = {
                                "total_stocks": 0,  
                                "high_score_stocks": 0,  # AI score >= 8
                                "score_sum": 0          # Sum of all scores
                            }
                        
                        # Update counts and sums
                        sectors_data[sector]["total_stocks"] += 1
                        sectors_data[sector]["score_sum"] += ai_score
                        
                        # Count high-score stocks
                        if ai_score >= 8:
                            sectors_data[sector]["high_score_stocks"] += 1
                
                # We only need to process one date entry
                break
            
            # Calculate metrics for each sector
            for sector, data in sectors_data.items():
                if data["total_stocks"] > 0:
                    # Calculate percentage of high-score stocks
                    data["high_score_percentage"] = (data["high_score_stocks"] / data["total_stocks"]) * 100
                    
                    # Calculate average score 
                    data["avg_score"] = data["score_sum"] / data["total_stocks"]
                    
                    # Calculate a combined quality metric (weighted average of both factors)
                    data["quality_metric"] = (0.7 * data["high_score_percentage"]) + (0.3 * data["avg_score"] * 10)
                    
                    print(f"Sector: {sector}, "
                          f"Avg Score: {data['avg_score']:.2f}, "
                          f"High-Score: {data['high_score_percentage']:.1f}%, "
                          f"Quality: {data['quality_metric']:.1f}, "
                          f"Stocks: {data['total_stocks']}")
            
            # Sort sectors by the quality metric (combined metric of high score % and average score)
            ranked_sectors = sorted(
                sectors_data.keys(),
                key=lambda s: sectors_data[s].get("quality_metric", 0),
                reverse=True
            )
            
            # Get top 5 sectors
            top_sectors = ranked_sectors[:5]
            print(f"Top 5 sectors: {top_sectors}")
            
            # Cache the result
            self.cache[cache_key] = top_sectors
            
            return top_sectors
            
        except Exception as e:
            print(f"Error calculating top sectors: {str(e)}")
            return []

    def get_top5_industrials_from_sectors(self) -> List[str]:
        # based on average AI?
        pass

    def return_the_top_tickers(self) -> List[str]:
        pass