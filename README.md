# TripleLift Solutions Challenge

**Prompt D: Write a script that will programmatically check whether all impressions pixels are valid.**

## Dependencies
- python
- pip
- requests 

## Required Packages
- Run `pip install requests`

## Running the Script 
- `tactic.csv` required in same directory  
- Run `python syncSolution.py` in command line

### Note
- Current version performs each `GET` check synchronously which has an efficiency of ~5 requests / second. Considering the number of URLs in the tactic.csv document, using an asynchronously library to simultaneously perform `GET` requests would be my optimization strategy to improve performance.
