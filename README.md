# IRR Miner
First commit

collector/main.py --> perform whois queries and saves rpsl objects as .txt files
extractor/extract.py --> fetch and parse communities semantics from whois collected data (.txt) through simple regex expressions 

OBS:
1. 'Collector' considers each server's daily query limits and adapts itself to systems where multiple users perform whois queries under the same IP address.
It intends to always perform a number of daily queries below the server's limit and to reduce it's number of daily queries when a new limit is achieved.
Very inefficient, but complete.

2. 'Extractor' considers a limited set of semantics.
It recognizes the following format:
"int:int SEMANTIC_TERM DESTINATION"
where DESTINATION is optional.
The regex used is primitive, can be reduced. 

