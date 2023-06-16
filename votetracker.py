import requests
import pandas as pd
import re


headers = {"X-API-Key": "3vXkCbyg2jHTaxq7wLnNdr2WPDn2lmRc1jBPx8KS"}

master = pd.DataFrame(columns=["Number", "Date", "Description", "Link", "MGP", "Jeffries", "Clark", "Hoyer", "AOC", "Jayapal", "Scalise", "Jim Jordan", "Rodgers", "MTG"])

# UPDATE THIS LINE WITH THE RANGE OF ROLL CALL NUMBERS YOU WANT DATA ABOUT
for i in range(1, 256):
    url = "https://api.propublica.org/congress/v1/118/house/sessions/1/votes/" + str(i+1) + ".json"
    try:
        req = requests.get(url, headers=headers)
        norm = pd.json_normalize(req.json())
        positions = pd.json_normalize(norm["results.votes.vote.positions"][0])
        date = (norm["results.votes.vote.date"])[0]
        source = (norm["results.votes.vote.source"])[0]
    except KeyError:
        continue

    try:
        description = (norm["results.votes.vote.question"])[0] + " " + (norm["results.votes.vote.bill.number"])[0]
        if (norm["results.votes.vote.question"])[0] == "On Agreeing to the Amendment":
            description = (norm["results.votes.vote.description"])[0]

    except KeyError:
        description = "error"

    try:
        mgp = str(positions.loc[positions['member_id'] == 'G000600']['vote_position'])
        jeffries = str(positions.loc[positions['member_id'] == 'J000294']['vote_position'])
        clark = str(positions.loc[positions['member_id'] == 'C001101']['vote_position'])
        hoyer = str(positions.loc[positions['member_id'] == 'H000874']['vote_position'])
        aoc = str(positions.loc[positions['member_id'] == 'O000172']['vote_position'])
        jayapal = str(positions.loc[positions['member_id'] == 'J000298']['vote_position'])
        scalise = str(positions.loc[positions['member_id'] == 'S001176']['vote_position'])
        jordan = str(positions.loc[positions['member_id'] == 'J000289']['vote_position'])
        rodgers = str(positions.loc[positions['member_id'] == 'M001159']['vote_position'])
        rodgers = str(positions.loc[positions['member_id'] == 'M001159']['vote_position'])
        greene = str(positions.loc[positions['member_id'] == 'G000596']['vote_position'])
   
        mgp = re.search(r'[A-Z][a-z]*', mgp)[0]
        jeffries = re.search(r'[A-Z][a-z]*', jeffries)[0]
        clark = re.search(r'[A-Z][a-z]*', clark)[0]
        hoyer = re.search(r'[A-Z][a-z]*', hoyer)[0]
        aoc = re.search(r'[A-Z][a-z]*', aoc)[0]
        jayapal = re.search(r'[A-Z][a-z]*', jayapal)[0]
        scalise = re.search(r'[A-Z][a-z]*', scalise)[0]
        jordan = re.search(r'[A-Z][a-z]*', jordan)[0]
        rodgers = re.search(r'[A-Z][a-z]*', rodgers)[0]
        greene = re.search(r'[A-Z][a-z]*', greene)[0]
    except KeyError:
        mgp = "Error"
        jeffries = "Error"
        clark = "Error"
        hoyer = "Error"
        aoc = "Error"
        jayapal = "Error"
        scalise = "Error"
        jordan = "Error"
        rodgers = "Error"
        greene = "Error"

    master.loc[len(master.index)] = [i+1, date, description, source, mgp, jeffries, clark, hoyer, aoc, jayapal, scalise, jordan, rodgers, greene]
    print(i)

print(master)
master.to_csv("out.csv", index=False)