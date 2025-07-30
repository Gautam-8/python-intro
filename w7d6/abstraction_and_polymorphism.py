from abc import ABC, abstractmethod

class MediaContent(ABC):

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def get_duration(self):
        pass

    @abstractmethod
    def get_file_size(self):    
        pass        

    @abstractmethod
    def calculate_streaming_cost(self):
        pass

    def add_rating(self, rating):
        if not hasattr(self, 'ratings'):
            self.ratings = []
        self.ratings.append(rating)


    def get_average_rating(self):
        if not hasattr(self, 'ratings') or not self.ratings:
            return 0
        return sum(self.ratings) / len(self.ratings)
    
    def is_premium_content(self):
        return hasattr(self, 'is_premium') and self.is_premium
    

class StreamingDevice(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def stream_content(self, content):
        pass

    @abstractmethod
    def adjust_quality(self, quality):
        pass

    def get_device_info(self):
        return f"{self.__class__.__name__} - {self.get_description()}"

    def check_compatibility(self, content):
        return True  # Default compatibility check
    


class Movie(MediaContent):
    def __init__(self, title, duration, resolution, genre, director, is_premium=False):
        self.title = title
        self.duration = duration  # in minutes
        self.resolution = resolution  # e.g., '1080p', '4K'
        self.genre = genre
        self.director = director
        self.is_premium = is_premium

    def play(self):
        return f"Playing movie: {self.title} ({self.resolution})"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return f"{self.duration * 100} MB"  # Simplified file size calculation

    def calculate_streaming_cost(self):
        return 5.99 if self.is_premium else 2.99
    
class TVShow(MediaContent):
    def __init__(self, title, genre, seasons, episodes, current_episode, is_premium=False):
        self.title = title
        self.genre = genre
        self.seasons = seasons
        self.episodes = episodes
        self.current_episode = current_episode
        self.is_premium = is_premium

    def play(self):
        return f"Playing TV Show: {self.title}, Season {self.current_episode[0]}, Episode {self.current_episode[1]}"

    def get_duration(self):
        return 45 * len(self.episodes) 

    def get_file_size(self):
        return f"{len(self.episodes) * 200} MB"  
    
    def calculate_streaming_cost(self):
        return 7.99 if self.is_premium else 3.99
    

class Podcast(MediaContent):
    def __init__(self, title, genre, episode_number, transcript_available, is_premium=False):
        self.title = title
        self.genre = genre
        self.episode_number = episode_number
        self.transcript_available = transcript_available
        self.is_premium = is_premium

    def play(self):
        return f"Playing Podcast: {self.title}, Episode {self.episode_number}"

    def get_duration(self):
        return 30  # Simplified duration for podcasts

    def get_file_size(self):
        return "50 MB"  # Simplified file size calculation

    def calculate_streaming_cost(self):
        return 1.99 if self.is_premium else 0.99
    

class Music(MediaContent):
    def __init__(self, title, genre, artist, album, lyrics_available, is_premium=False):
        self.title = title
        self.genre = genre
        self.artist = artist
        self.album = album
        self.lyrics_available = lyrics_available
        self.is_premium = is_premium

    def play(self):
        return f"Playing Music: {self.title} by {self.artist}"

    def get_duration(self):
        return 3  # Simplified duration for music tracks

    def get_file_size(self):
        return "5 MB"  # Simplified file size calculation

    def calculate_streaming_cost(self):
        return 0.99 if self.is_premium else 0.49
    

# Streaming Devices
class SmartTV(StreamingDevice):
    def __init__(self, model, screen_size, supports_4k=True):
        self.model = model
        self.screen_size = screen_size
        self.supports_4k = supports_4k

    def connect(self):
        return f"Connecting SmartTV: {self.model}"

    def stream_content(self, content):
        return f"Streaming {content.title} on SmartTV"

    def adjust_quality(self, quality):
        return f"Adjusting quality to {quality} on SmartTV"

    def get_description(self):
        return f"Model: {self.model}, Screen Size: {self.screen_size}, 4K Support: {self.supports_4k}"
    
class Laptop(StreamingDevice):
    def __init__(self, model, screen_size, cpu=None):
        self.model = model
        self.screen_size = screen_size
        self.cpu = cpu

    def connect(self):
        return f"Connecting Laptop: {self.model}"

    def stream_content(self, content):
        return f"Streaming {content.title} on Laptop"

    def adjust_quality(self, quality):
        return f"Adjusting quality to {quality} on Laptop"

    def get_description(self):
        return f"Model: {self.model}, Screen Size: {self.screen_size}"
    

class Mobile(StreamingDevice):
    def __init__(self, model, os, screen_size):
        self.model = model
        self.os = os
        self.screen_size = screen_size

    def connect(self):
        return f"Connecting Mobile: {self.model}"

    def stream_content(self, content):
        return f"Streaming {content.title} on Mobile"

    def adjust_quality(self, quality):
        return f"Adjusting quality to {quality} on Mobile"

    def get_description(self):
        return f"Model: {self.model}, Screen Size: {self.screen_size}"
    

class SmartSpeaker(StreamingDevice):
    def __init__(self, model, assistant=None, supports_voice=True):
        self.model = model
        self.assistant = assistant
        self.supports_voice = supports_voice

    def connect(self):
        return f"Connecting Smart Speaker: {self.model}"
    def stream_content(self, content):
        # Only allow audio content (Podcast, Music)
        if isinstance(content, Podcast) or isinstance(content, Music):
            return {"status": "success", "quality": "audio", "message": f"Streaming {content.title} on Smart Speaker"}
        else:
            return {"status": "error", "quality": None, "message": "Audio only device: cannot stream video content."}
    def adjust_quality(self, quality):
        return f"Adjusting quality to {quality} on Smart Speaker"
    


    # Test Case 1: Abstract class instantiation should fail
try:
    content = MediaContent("Test", "Test Category")
    assert False, "Should not be able to instantiate abstract class"
except TypeError:
    pass

try:
    device = StreamingDevice("Test Device")
    assert False, "Should not be able to instantiate abstract class"
except TypeError:
    pass

# Test Case 2: Polymorphic content creation and playback
movie = Movie("Inception", 148, "4K", "Sci-Fi", "Christopher Nolan")
tv_show = TVShow("Breaking Bad", "Drama", 5, list(range(1,63)), (5,1))
podcast = Podcast("Tech Talk", "Technology", 45, True)
music = Music("Bohemian Rhapsody", "Rock", "Queen", "A Night at the Opera", True)

contents = [movie, tv_show, podcast, music]

# All should implement required abstract methods
for content in contents:
    play_result = content.play()
    assert isinstance(play_result, str)
    assert "playing" in play_result.lower()

    duration = content.get_duration()
    assert isinstance(duration, (int, float))
    assert duration > 0

    file_size = content.get_file_size()
    assert isinstance(file_size, str)

    cost = content.calculate_streaming_cost()
    assert isinstance(cost, (int, float))
    assert cost >= 0

# Test Case 3: Device-specific streaming behavior
smart_tv = SmartTV("Samsung 4K TV", "55 inch", True)
laptop = Laptop("MacBook Pro", "13 inch", "Intel i7")
mobile = Mobile("iPhone 13", "iOS", 85)
speaker = SmartSpeaker("Amazon Echo", "Alexa", True)

devices = [smart_tv, laptop, mobile, speaker]

for device in devices:
    connect_result = device.connect()
    assert "connect" in connect_result.lower()

    # Test polymorphic streaming
    if isinstance(device, SmartSpeaker):
        stream_result = device.stream_content(movie)
        assert isinstance(stream_result, dict)
        assert "quality" in stream_result
        assert "status" in stream_result
    else:
        stream_result = device.stream_content(movie)
        assert isinstance(stream_result, str)

# Test Case 4: Device-content compatibility
# Smart speaker should only play audio content
audio_content = [podcast, music]
video_content = [movie, tv_show]

for content in audio_content:
    result = speaker.stream_content(content)
    assert result["status"] == "success"

for content in video_content:
    result = speaker.stream_content(content)
    assert result["status"] == "error" or "audio only" in result.get("message", "")


class User:
    def __init__(self, username, subscription_tier, preferences):
        self.username = username
        self.subscription_tier = subscription_tier
        self.preferences = preferences 
        self.watch_history = []

    def add_to_watch_history(self, content):
        self.watch_history.append(content)

    def get_watch_history(self):
        return self.watch_history
    

class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.content_library = []
        self.devices = {}

    def add_content(self, content):
        self.content_library.append(content)

    def register_user(self, user):
        self.users.append(user)

    def register_device(self, device, user):
        if user.username not in self.devices:
            self.devices[user.username] = []
        self.devices[user.username].append(device)

    def get_recommendations(self, user):
        recommendations = []
        for content in self.content_library:
            if content.genre in user.preferences or content.is_premium_content():
                recommendations.append(content)
        return recommendations

    def start_watching(self, user, content, device):
        if user.subscription_tier == "Free" and content.is_premium_content():
            return {"status": "error", "message": "Subscription required: Upgrade to premium to watch this content."}
        
        if device.check_compatibility(content):
            user.add_to_watch_history(content)
            return {"status": "started", "content": content.title}
        else:
            return {"status": "error", "message": "Device not compatible with this content."}

    def get_user_analytics(self, user):
        total_watch_time = sum(content.get_duration() for content in user.watch_history)
        favorite_genres = {content.genre for content in user.watch_history}
        return {
            "total_watch_time": total_watch_time,
            "favorite_genres": list(favorite_genres)
        }
# Test Case 5: User subscription and platform integration
user = User("john_doe", "Premium", ["Sci-Fi", "Drama"])
platform = StreamingPlatform("NetStream")



# Add content to platform
for content in contents:
    platform.add_content(content)

# Register user and device
platform.register_user(user)
platform.register_device(smart_tv, user)

# Test recommendation system
recommendations = platform.get_recommendations(user)
assert isinstance(recommendations, list)
assert len(recommendations) > 0

# Test watch history and analytics
watch_session = platform.start_watching(user, movie, smart_tv)
assert watch_session["status"] == "started"

analytics = platform.get_user_analytics(user)
assert "total_watch_time" in analytics
assert "favorite_genres" in analytics

# Test Case 6: Subscription tier restrictions
free_user = User("jane_doe", "Free", ["Comedy"])
platform.register_user(free_user)

# Premium content should be restricted for free users
premium_movie = Movie("Premium Film", "Action", 120, "4K", "Director")
premium_movie.is_premium = True
platform.add_content(premium_movie)

watch_attempt = platform.start_watching(free_user, premium_movie, laptop)
assert watch_attempt["status"] == "error"
assert "subscription" in watch_attempt["message"].lower()

# Test Case 7: Content rating and recommendation impact
movie.add_rating(4.5)
movie.add_rating(4.8)
movie.add_rating(4.2)

assert abs(movie.get_average_rating() - 4.5) < 0.1

# Highly rated content should appear in recommendations
new_recommendations = platform.get_recommendations(user)
highly_rated = [content for content in new_recommendations if content.get_average_rating() > 4.0]
assert len(highly_rated) > 0
