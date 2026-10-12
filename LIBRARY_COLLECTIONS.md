# Library Collections

`Library Collections` is the third top-level Nuvio collection, alongside `Streaming Services` and `Explore & Discover`.

## Behavior

- Movie franchise membership is discovered from TMDB's `belongs_to_collection` metadata.
- A folder is generated only when at least one matching movie exists in the current local database and is visible to the requesting token.
- The folder artwork uses TMDB collection poster/backdrop paths, falling back to artwork from a locally available movie.
- Folder catalogs return only database-backed movies in the collection, sorted by release year and then title. Unavailable TMDB franchise titles are not exposed as local items.
- The existing Nuvio profile endpoint `/stremio/{token}/nuvio-collection.json` now returns all three sections.
- A standalone profile endpoint is available at `/stremio/{token}/nuvio-library-collections.json` (also `/stremio/{token}/nuvio-library-collection.json`).

## Cache and first-time indexing

Collection metadata is stored in the tracking database's `library_collection_cache` collection. A background refresh scans positive TMDB movie IDs across `storage_*` databases, requests each movie's collection metadata, and persists the result. Positive and negative lookups are cached; stale entries are rechecked after 90 days. The scan is throttled between runs and uses a small number of concurrent TMDB requests.

The backend must have a valid TMDB API key configured. On a new deployment, the first profile request may show only the groups already cached while the background index is filling; refresh the Nuvio profile after indexing has progressed. New/uncached movies are discovered by the next index refresh (normally within five minutes after a completed scan).

The profile and catalog routes apply the existing token visibility and exclusive-catalog filters before exposing local titles. Collection metadata itself is global cache data; a collection is only shown to a token if that token can see at least one member movie.

## Tests

Run the metadata unit tests in an environment with the project's dependencies installed:

```bash
python -m unittest tests.test_local_collections
python -m compileall -q Backend
```

TV-universe groupings are not included in this initial implementation because TMDB's `belongs_to_collection` relationship is movie-franchise oriented. They can be added later through a separate relationship source or configured mapping.
