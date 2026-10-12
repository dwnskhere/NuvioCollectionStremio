# Explore & Discover metadata fallback fix

## What was going wrong

The Nuvio collection JSON and Telegram add-on manifest use a matching add-on ID, and the `India` folder's Bollywood catalog ID is present in the manifest. The collection URL itself is not the cause.

The backend's `/meta/{media_type}/{id}.json` route previously returned an empty `meta` object whenever an item was not in the Telegram media database. That made Nuvio's detail screen fail for otherwise valid TMDB/Trakt collection entries that had no matching database row. In addition, the manifest did not advertise the `tmdb` ID prefix, and the stream route treated TMDB-prefixed IDs as if the literal string `tmdb` were an IMDb ID.

## Changes made

- Added parsing for `tmdb:movie:<id>`, `tmdb:tv:<id>`, `tmdb:<id>`, and season/episode suffixes, without changing the existing IMDb/Kitsu formats.
- Added an external metadata fallback for unindexed IMDb IDs using Cinemeta and for TMDB IDs using the configured TMDB API.
- Added TMDB-ID database lookups and disambiguated movies from series when their numeric TMDB IDs happen to be equal.
- Advertised the `tmdb` ID prefix only when the backend has a configured TMDB API key.
- Kept the existing stream behavior: if no Telegram/global stream is found, return the existing Public Request Page action, now using a resolved title (and season/episode when applicable) rather than a raw provider ID where metadata is available.

No collection JSON or token values were changed.

## Validation

- Python syntax compilation passed for `Backend/`.
- Six ID parsing regression cases passed for IMDb, Kitsu, and TMDB IDs.
- A mocked database test passed for TMDB movie-vs-series ID disambiguation.
- A live end-to-end test of the patched code against the hosted service was not possible from the build sandbox; the patch must be deployed before validating it in Nuvio.

## Deployment checklist

1. Deploy the two changed Python files: `Backend/fastapi/routes/stremio_routes.py` and `Backend/helper/database.py`.
2. For TMDB-only IDs (IDs that do not resolve to an IMDb `tt...` ID), ensure the backend's TMDB API key is configured.
3. Refresh or reinstall the Telegram add-on in Nuvio so it reloads the updated manifest `idPrefixes`.
4. Refresh Explore & Discover and open a title that is not in the Telegram database. Its details should load; when no stream exists, the Telegram stream list should expose the existing Request Media action.
