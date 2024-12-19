import unittest
from unittest.mock import patch, mock_open
from neural_network_main import (
    load_mood_playlist_mapping,
    get_playlist_link,
    extract_dominant_emotion,
    find_playlist,
    process_analysis_result
)

class TestFaceAnalysis(unittest.TestCase):

    def test_load_mood_playlist_mapping_valid(self):
        mock_json = '{"happy": "https://soundcloud.com/happy_playlist"}'
        with patch("builtins.open", mock_open(read_data=mock_json)):
            mapping = load_mood_playlist_mapping("test.json")
        self.assertEqual(mapping, {"happy": "https://soundcloud.com/happy_playlist"})

    def test_load_mood_playlist_mapping_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            mapping = load_mood_playlist_mapping("missing.json")
        self.assertEqual(mapping, {})

    def test_load_mood_playlist_mapping_invalid_json(self):
        invalid_json = '{"happy": "https://soundcloud.com/happy_playlist"'
        with patch("builtins.open", mock_open(read_data=invalid_json)):
            mapping = load_mood_playlist_mapping("invalid.json")
        self.assertEqual(mapping, {})

    def test_extract_dominant_emotion(self):
        emotion_data = {"dominant_emotion": "sad", "happy": 0.1, "sad": 0.9}
        dominant_emotion = extract_dominant_emotion(emotion_data)
        self.assertEqual(dominant_emotion, "sad")

    def test_extract_dominant_emotion_default(self):
        emotion_data = {}
        dominant_emotion = extract_dominant_emotion(emotion_data)
        self.assertEqual(dominant_emotion, "neutral")

    def test_find_playlist_existing_emotion(self):
        playlist_mapping = {"happy": "https://soundcloud.com/happy_playlist"}
        playlist_link = find_playlist("happy", playlist_mapping)
        self.assertEqual(playlist_link, "https://soundcloud.com/happy_playlist")

    def test_find_playlist_default(self):
        playlist_mapping = {"sad": "https://soundcloud.com/sad_playlist"}
        playlist_link = find_playlist("happy", playlist_mapping)
        self.assertEqual(playlist_link, "https://soundcloud.com/search?q=default playlist")

    def test_process_analysis_result_list(self):
        result = [{"age": 25, "gender": "Man"}]
        processed_result = process_analysis_result(result)
        self.assertEqual(processed_result, {"age": 25, "gender": "Man"})

    def test_process_analysis_result_dict(self):
        result = {"age": 30, "gender": "Woman"}
        processed_result = process_analysis_result(result)
        self.assertEqual(processed_result, {"age": 30, "gender": "Woman"})

if __name__ == "__main__":
    unittest.main()