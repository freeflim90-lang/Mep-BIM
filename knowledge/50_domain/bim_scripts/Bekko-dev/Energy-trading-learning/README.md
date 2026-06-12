# Energy Trading Learning

Weekly analysis of European power markets using Python and public data sources.

## Why this repo
I'm an energy engineer with 5 years managing multi-energy portfolios (€30M+).
I'm transitioning toward energy trading & risk management.
This repo tracks my learning journey — market analysis, Python tools, and ETRM concepts.

## This week's observations (22 March 2026)
- Classic duck curve pattern on French spot prices — solar generation compressed 
  midday prices while morning/evening demand peaks pushed prices to highs
- Merit order in action : renewable surplus in Spain/Portugal depressed French 
  prices via market coupling during peak solar hours
- France remained net exporter throughout the week — nuclear baseload enabling 
  consistent export to neighbors

## Contents
- `scripts/` — Python scripts for market data analysis
- `data/` — EPEX and RTE spot price datasets
- `notes/` — ETRM concepts and definitions (merit order, VaR, futures, swaps...)

## Stack
Python · Pandas · Matplotlib · Requests

## Data sources
- RTE éCO2mix (real-time French power market data)
- EPEX SPOT public data
