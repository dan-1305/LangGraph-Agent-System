import os
import sys
import io
import tweepy
from dotenv import load_dotenv

if sys.stdout is not None:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

# Load môi trường
load_dotenv()

class XApiClient:
    """
    Client gọi Twitter API v2 để cày Social Point.
    Yêu cầu các keys trong file .env:
    TWITTER_API_KEY
    TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_SECRET
    TWITTER_BEARER_TOKEN (Nếu cần cho Read-only)
    """
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # Init tweepy client v2
        if all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret
            )
            self.is_connected = True
        else:
            print("⚠️ Thiếu cấu hình Twitter API trong .env")
            self.is_connected = False

    def get_me(self):
        """Lấy thông tin tài khoản đang login"""
        if not self.is_connected:
            return None
        try:
            response = self.client.get_me()
            if response and response.data:
                print(f"✅ Đã kết nối với X (Twitter) dưới tên: @{response.data.username} (ID: {response.data.id})")
                return response.data
            return None
        except Exception as e:
            print(f"❌ Lỗi khi lấy thông tin User: {e}")
            return None

    def post_tweet(self, text: str):
        """Đăng 1 dòng Tweet mới"""
        if not self.is_connected:
            return False
        try:
            response = self.client.create_tweet(text=text)
            print(f"✅ Đăng Tweet thành công! ID: {response.data['id']}")
            return response.data['id']
        except Exception as e:
            print(f"❌ Lỗi khi đăng Tweet: {e}")
            return False

    def like_tweet(self, tweet_id: str):
        """Like 1 tweet"""
        if not self.is_connected:
            return False
        try:
            response = self.client.like(tweet_id)
            print(f"✅ Đã Like Tweet {tweet_id}! Trạng thái: {response.data}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi Like Tweet: {e}")
            return False

    def retweet(self, tweet_id: str):
        """Retweet (Repost)"""
        if not self.is_connected:
            return False
        try:
            response = self.client.retweet(tweet_id)
            print(f"✅ Đã Retweet {tweet_id}! Trạng thái: {response.data}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi Retweet: {e}")
            return False

if __name__ == "__main__":
    client = XApiClient()
    if client.is_connected:
        user_info = client.get_me()
        if user_info:
            print(f"Chạy test thành công! Bạn có thể gọi client.post_tweet('Hello World') nếu cần.")
    else:
        print("Vui lòng bổ sung API Keys vào file .env")
