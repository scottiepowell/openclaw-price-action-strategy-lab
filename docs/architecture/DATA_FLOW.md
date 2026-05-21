# Data Flow

## Flow

1. Course evidence is captured in the archiver repo.
2. Historical OHLCV data is prepared in the data extraction repo.
3. Strategy Lab records references, manifests, and crosswalks.
4. Replay cases and contradiction cases are labeled.
5. Candidate maturity is refined conservatively.
6. Paper-validation artifacts are stored separately.

## Boundary

- Reference-first, not raw-data-first.
- No live-trading path.
