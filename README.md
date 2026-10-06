# Fossil Island Dataworks

A WIP data pipeline that fetches Grand Exchange data for analytics purposes.

## Rough pipeline

Get JSON data → Stick into S3-like SeaweedFS filesystem → Run ETL pipeline to transform prices and inner join with mappings → Stick into prototype Postgres warehouse → TBD

## Endpoints used for data

`/latest` → Latest GE prices

`/mappings` → All OSRS items

## Services

SeaweedFS as a data lake for the mapping and prices data
Postgres as a prototype warehouse for the inner joined mappings and prices

See docker/ for configuration

## Commands

`start` → Start all Docker containers

`stop` → Stop all Docker containers

`format` → Ruff format all files

`lint` → Ruff lint all files

`fix` → Apply formatting and lint fixes to all files

`source` → Activate venv and env

`test` → Run full pytest checks

`run` → Run E2E pipeline through entry point
