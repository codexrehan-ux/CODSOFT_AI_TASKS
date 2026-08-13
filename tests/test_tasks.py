"""Automated regression tests for the CodSoft AI internship projects."""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


chatbot = load_module("test_chatbot", "Task-1-Rule-Based-Chatbot/chatbot.py")
tictactoe = load_module("test_tictactoe", "Task-2-Tic-Tac-Toe-AI/tic_tac_toe.py")
recommender = load_module("test_recommender", "Task-4-Recommendation-System/recommendation_system.py")


class TestChatbot(unittest.TestCase):
    def test_common_rules(self):
        self.assertIn("Hello", chatbot.get_response("HELLO"))
        self.assertIn("Artificial Intelligence", chatbot.get_response("what is AI?"))
        self.assertIn("Machine Learning", chatbot.get_response("what is machine learning?"))
        self.assertEqual("You're welcome!", chatbot.get_response("thank you"))

    def test_unknown_input(self):
        response = chatbot.get_response("tell me about underwater basket weaving")
        self.assertIn("don't understand", response)


class TestTicTacToe(unittest.TestCase):
    def test_winner_detection(self):
        board = [
            ["X", "X", "X"],
            ["O", " ", "O"],
            [" ", " ", " "],
        ]
        self.assertEqual(tictactoe.HUMAN, tictactoe.check_winner(board))

    def test_ai_takes_immediate_win(self):
        board = [
            ["O", "O", " "],
            ["X", "X", " "],
            [" ", " ", " "],
        ]
        self.assertEqual((0, 2), tictactoe.best_ai_move(board))

    def test_ai_blocks_immediate_loss(self):
        board = [
            ["X", "X", " "],
            ["O", " ", " "],
            [" ", " ", "O"],
        ]
        self.assertEqual((0, 2), tictactoe.best_ai_move(board))

    def test_no_move_on_full_board(self):
        board = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"],
        ]
        self.assertEqual([], tictactoe.available_moves(board))
        self.assertIsNone(tictactoe.best_ai_move(board))


class TestRecommendationSystem(unittest.TestCase):
    def test_exact_and_fuzzy_title_search(self):
        self.assertIsNotNone(recommender.find_movie("Inception"))
        self.assertIsNotNone(recommender.find_movie("Incepton"))

    def test_recommendations_are_ranked_and_exclude_selected(self):
        selected, results = recommender.recommend("Inception")
        self.assertEqual("Inception", selected["title"])
        self.assertEqual(5, len(results))
        self.assertNotIn("Inception", [title for _, title in results])
        scores = [score for score, _ in results]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertTrue(all(0 <= score <= 1 for score in scores))

    def test_unknown_movie(self):
        selected, results = recommender.recommend("This Movie Does Not Exist")
        self.assertIsNone(selected)
        self.assertEqual([], results)


class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("portfolio_app", ROOT / "app.py")
        cls.app_module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.app_module)
        cls.client = cls.app_module.app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"AI Project Lab", response.data)

    def test_chat_api(self):
        response = self.client.post("/api/chat", json={"message": "hello"})
        self.assertEqual(200, response.status_code)
        self.assertIn("Hello", response.json["response"])

    def test_chat_empty_input(self):
        response = self.client.post("/api/chat", json={"message": ""})
        self.assertEqual(400, response.status_code)

    def test_movie_api(self):
        response = self.client.get("/api/movies")
        self.assertEqual(200, response.status_code)
        self.assertIn("Inception", response.json["movies"])

    def test_recommendation_api(self):
        response = self.client.post("/api/recommend", json={"title": "Inception"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.json["recommendations"]))

    def test_invalid_tictactoe_board(self):
        response = self.client.post("/api/tictactoe", json={"board": ["X"]})
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()
