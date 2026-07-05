from core_utilities.http_client import HTTPClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
HEADERS = {"Authorization": PEXELS_API_KEY}
VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"

from projects.auto_affiliate_video.src.video_telemetry import measure_latency

class PexelClient:
    """A client for interacting with the Pexels API to find and download videos."""

    @measure_latency("fetch_broll")
    def find_and_download_video(self, query: str, output_path: str) -> str:
        """
        Searches for a video on Pexels and downloads the most relevant one.

        Args:
            query (str): The search term for the video.
            output_path (str): The path to save the downloaded video.

        Returns:
            str: The path to the downloaded video, or an empty string if failed.
        """
        if not PEXELS_API_KEY:
            print("PEXELS_API_KEY not found in environment variables.")
            return ""

        params = {"query": query, "per_page": 5, "orientation": "portrait"}
        
        try:
            response = HTTPClient.get(VIDEO_SEARCH_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("videos"):
                print(f"No videos found for query: {query}")
                return ""

            # Find the best quality video link
            video_to_download = data["videos"][0] # Simple approach: take the first one
            video_links = video_to_download.get("video_files", [])
            
            best_link = self._get_best_quality_link(video_links)
            if not best_link:
                print("No suitable video file found.")
                return ""

            # Download the video
            video_response = HTTPClient.get(best_link, stream=True)
            video_response.raise_for_status()
            
            with open(output_path, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Video downloaded successfully to: {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"An error occurred with the Pexels API request: {e}")
            return ""

    def _get_best_quality_link(self, video_links: list) -> str:
        """Selects the best quality video link that is under a certain size if needed."""
        # For now, we just find the one with the highest resolution.
        # A more advanced version could check file size.
        best_link = ""
        max_width = 0
        for link in video_links:
            if link.get("quality") == "hd" and link.get("width", 0) > max_width:
                 max_width = link["width"]
                 best_link = link["link"]
        return best_link

if __name__ == '__main__':
    # Example usage
    client = PexelClient()
    # You need to have PEXELS_API_KEY in your .env file to run this
    if PEXELS_API_KEY:
        client.find_and_download_video("galaxy", "galaxy_video.mp4")


