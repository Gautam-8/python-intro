from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, text):
        """
        Initialize with text to analyze
        Args:
            text (str): Text to analyze
        """
        self.original_text = text
        self.text = text.lower()  # For case-insensitive analysis

    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character
        Args:
            include_spaces (bool): Whether to include spaces in count
        Returns:
            Counter: Character frequencies
        """
        counter = Counter(self.text if include_spaces else self.text.replace(' ', ''))
        return counter

    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word (minimum length filter)
        Args:
            min_length (int): Minimum word length to include
        Returns:
            Counter: Word frequencies
        """
        words = self.text.split()
        filtered_words = [word for word in words if len(word) >= min_length]   
        return Counter(filtered_words)

    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words)
        Returns:
            dict: Contains 'lengths' (Counter), 'average', 'longest', 'shortest'
        """
        sentences = re.split(r'[.!?]+', self.text)
        lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
        avg_length = sum(lengths) / len(lengths) if lengths else 0
        longest = max(lengths) if lengths else 0
        shortest = min(lengths) if lengths else 0
        return {
                'lengths': Counter(lengths),
                'average': avg_length,
                'longest': longest,
                'shortest': shortest
               }

    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding very common English words
        Args:
            n (int): Number of words to return
            exclude_common (bool): Exclude common words like 'the', 'and', etc.
        Returns:
            list: List of tuples (word, count)
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
                        'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        word_freq = self.get_word_frequency()
        if exclude_common:
            word_freq = {word: count for word, count in word_freq.items() if word not in common_words}
        sorted_words = Counter(word_freq).most_common(n)
        return sorted_words

    def get_reading_statistics(self):
        """
        Get comprehensive reading statistics
        Returns:
            dict: Contains character_count, word_count, sentence_count,
                  average_word_length, reading_time_minutes (assume 200 WPM)
        """
        words = self.text.split()
        character_count = len(self.text)
        word_count = len(words)
        sentence_count = len(re.split(r'[.!?]+', self.text)) - 1
        average_word_length = character_count / word_count if word_count > 0 else 0
        reading_time_minutes = word_count / 200  
        return {
            'character_count': character_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_word_length': average_word_length,
            'reading_time_minutes': reading_time_minutes
        }

    def compare_with_text(self, other_text):
        """
        Compare this text with another text
        Args:
            other_text (str): Text to compare with
        Returns:
            dict: Contains 'common_words', 'similarity_score', 'unique_to_first', 'unique_to_second'
        """
        other_analyzer = TextAnalyzer(other_text)
        common_words = set(self.get_word_frequency().keys()) & set(other_analyzer.get_word_frequency().keys())
        unique_to_first = set(self.get_word_frequency().keys()) - common_words 
        unique_to_second = set(other_analyzer.get_word_frequency().keys()) - common_words
        similarity_score = len(common_words) / (len(self.get_word_frequency()) + len(other_analyzer.get_word_frequency()) - len(common_words)) if (len(self.get_word_frequency()) + len(other_analyzer.get_word_frequency())) > 0 else 0
        return {    
            'common_words': common_words,
            'similarity_score': similarity_score,
            'unique_to_first': unique_to_first,
            'unique_to_second': unique_to_second
        }


# Test your implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
make it very attractive for Rapid Application Development. Python is simple, easy to learn
syntax emphasizes readability and therefore reduces the cost of program maintenance.
Python supports modules and packages, which encourages program modularity and code reuse.
The Python interpreter and the extensive standard library are available in source or binary
form without charge for all major platforms, and can be freely distributed.
"""

analyzer = TextAnalyzer(sample_text)
print("Character frequency (top 5):", analyzer.get_character_frequency().most_common()[:5])
print("Word frequency (top 5):", analyzer.get_word_frequency().most_common()[:5])
print("Common words:", analyzer.find_common_words(5))
print("Reading statistics:", analyzer.get_reading_statistics())

# Compare with another text
other_text = "Java is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(other_text)
print("Comparison results:", comparison)
