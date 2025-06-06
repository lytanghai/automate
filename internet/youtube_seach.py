from googleapiclient.discovery import build
import datetime

# Replace with your actual API key
API_KEY = "AIzaSyAjdPDeBvyl64FmGRf9EsspjAuuiR5tAW8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search_youtube(query, published_after="2020-10-23T00:00:00Z", max_results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Fetch up to 50 videos (search API max limit per call)
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        type="video",
        order="viewCount",
        maxResults=50,
        publishedAfter=published_after
    ).execute()

    results = []
    for item in search_response["items"]:
        if len(results) >= max_results:
            break

        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]

        # Get view count
        video_response = youtube.videos().list(
            id=video_id,
            part="statistics"
        ).execute()

        view_count = int(video_response["items"][0]["statistics"].get("viewCount", 0))

        if view_count >= 1_000_000:
            results.append({
                "title": video_title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "views": view_count
            })

    return results

def main():
    topic = input("Enter a topic to learn: ")
    num_results = input("How many results do you want (e.g., 5 or 10)? ")

    try:
        max_results = int(num_results)
    except ValueError:
        print("Invalid number. Defaulting to 5.")
        max_results = 5

    print("\nSearching YouTube...")

    videos = search_youtube(topic, max_results=max_results)

    if not videos:
        print("No results found matching criteria.")
        return

    print("\nTop YouTube Videos:")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}")
        print(f"   {video['url']} (Views: {video['views']:,})")

if __name__ == "__main__":
    main()
