"""Unit tests for TMDB franchise metadata normalization."""
import unittest
from types import SimpleNamespace

from Backend.helper.local_collections import _parse_collection_details, tmdb_image_url


class LocalCollectionMetadataTests(unittest.TestCase):
    def test_normalizes_movie_collection_details(self):
        details = SimpleNamespace(
            belongs_to_collection=SimpleNamespace(
                id=1241,
                name="Harry Potter Collection",
                poster_path="/poster.jpg",
                backdrop_path="/backdrop.jpg",
            )
        )

        result = _parse_collection_details(details, 671)

        self.assertEqual(result["tmdb_id"], 671)
        self.assertEqual(result["collection_id"], 1241)
        self.assertEqual(result["collection_name"], "Harry Potter Collection")
        self.assertEqual(result["poster_path"], "/poster.jpg")
        self.assertIsNotNone(result["checked_at"])

    def test_normalizes_dict_payload(self):
        result = _parse_collection_details(
            {
                "belongs_to_collection": {
                    "id": "999",
                    "name": "Example Franchise",
                    "poster_path": "/example.jpg",
                    "backdrop_path": None,
                }
            },
            123,
        )
        self.assertEqual(result["collection_id"], 999)
        self.assertEqual(result["collection_name"], "Example Franchise")

    def test_handles_movie_without_collection(self):
        result = _parse_collection_details({"belongs_to_collection": None}, 321)
        self.assertIsNone(result["collection_id"])
        self.assertIsNone(result["collection_name"])

    def test_tmdb_image_urls(self):
        self.assertEqual(
            tmdb_image_url("/poster.jpg"),
            "https://image.tmdb.org/t/p/w500/poster.jpg",
        )
        self.assertEqual(
            tmdb_image_url("/backdrop.jpg", "w1280"),
            "https://image.tmdb.org/t/p/w1280/backdrop.jpg",
        )
        self.assertEqual(tmdb_image_url("https://example.test/p.jpg"), "https://example.test/p.jpg")
        self.assertIsNone(tmdb_image_url(None))


if __name__ == "__main__":
    unittest.main()
