import os
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime
from danelfin_api import DanelfinAPIClient

def get_date() -> str:
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    input_date = input(f"Enter a date (YYYY-MM-DD) [default: {current_date}]: ")
    return input_date or current_date




def danelfin_environment() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Get Danelfin API environment variables."""
    # Load environment variables from .env file
    load_dotenv()

    danelfin_api_key = os.getenv("DANELFIN_API_KEY")
    danelfin_api_url = os.getenv("DANELFIN_API_URL")
    danelfin_api_ranking_url = os.getenv("DENELFIN_API_RANKING_URL")  # Fixed typo in variable name

    return danelfin_api_key, danelfin_api_url, danelfin_api_ranking_url


def main():
    """Main function to run the Danelfin API client."""
    # get date
    current_date = get_date()
    # Get environment variables
    danelfin_api_key, danelfin_api_url, danelfin_api_ranking_url = danelfin_environment()

    # Initialize the API client
    danelfin_api_client = DanelfinAPIClient(
        date=current_date,
        api_key=danelfin_api_key,
        api_url=danelfin_api_url,
        ranking_url=danelfin_api_ranking_url
    )

    # print sectors

    top5_sectors = danelfin_api_client.get_top5_sectors()




if __name__ == "__main__":
    main()


