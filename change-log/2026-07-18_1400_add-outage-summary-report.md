# Change Log — Add outage summary report endpoint

**Date:** 2026-07-18
**PR:** test/openpages-smoke-fail
**Author:** bryanyang
**Type:** feature

## Summary
Added `/reports/outage-summary` endpoint that returns outage counts grouped
by region with average duration. Supports optional `?region=` filter.

## Files changed
- `api/reports.py` — added outage summary route
