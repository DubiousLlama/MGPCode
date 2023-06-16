# MGPCode

How to estimate the Lugar Score the manual way:

1.	For each member, count the number of opposite-party bills they’ve cosponsored and the total number of bills they’ve cosponsored. Record them in the HumanReadableLugar spreadsheet. It is currently up to date as of June 5.
2.	For each member, count how many bills they’ve sponsored, how many have an opposite-party cosponsor and how many opposite-party cosponsors it has
3.	Calculate the percentage of their sponsored and cosponsored bills that are bipartisan by these metrics
4.	Calculate their bipartisan intensity by taking the base-2 logarithm of the average number of opposite-party cosponsors they have on their bills.
5.	You can stop here and just compare based on these metrics to see how you stack up.
6.	If you want extra credit, you can standardize each of these data points using the average and standard deviation for members of the same party, then take a weighted average of these standardized. I use a weighting of 30% percentage cosponsorships that are bipartisan, 30% percentage of sponsored bills that are bipartisan, 20% bipartisan intensity, and 10% each for absolute number of bipartisan bills sponsored and cosponsored.

Forward this to the new interns if any of them are technically inclined:
To do things the automated way:
-	Install python (you can do this from the windows store
-	Run ‘python3 -m pip install pandas’ and ‘python3 -m pip install numpy’
-	Place the attached python file on the desktop
-	Edit the ‘lugarcalculator.py’ file to update the list of commemorative coin and post office naming bills at the top
-	Run ‘cd Desktop’ then ‘python3 -m lugarcalculator.py’
-	Wait for 1-2 hours for it to do its thing. Progress updates will print to the terminal.
-	The script will output data to ‘lugar.csv’ for summary statistics and ‘HumanReadableLugar.xlsx’ for the bill lists
-	Use the summary statistics to calculate lugar scores same as you would for the manual way.

Automatic vote tracker updates using votetracker.py:
-	This task isn’t so bad to do by hand so only use this if you feel like it
-	Before running, update line #11 with the range of votes you want data on
-	Run the python file and wait a few minutes- it will output to a file called ‘out.csv’
-	I made this poorly because I wanted to do it as quickly as possible. Don’t judge my code please.
