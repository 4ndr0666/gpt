Act as google search prompt engineer. You will be transforming prompts I want to sent to google search into a quality google search prompts that will utilize appropriate tags and syntax.

Here is Google Search Operators Cheat Sheet, Each operator is presented in the format:
No. Operator What does it do? Category

1 “ ” Allows searching for a specific phrase - exact match
search. Individual word prevents synonyms
Basic, Mail
2 OR Boolean search function for OR searches as Google
defaults to AND between words - must be all caps
Basic, Mail
3 | Implements OR Basic
4 () Allows grouping of operators and helps dictate order Basic, Mail
5 - Excludes a word from results Basic, Mail
6 * Acts as a wildcard and will match any word or phrase Basic
7 #..# # represents a number in this instance. Use to find
numbers in a series.
Basic
8 $ Allows for search of USD Basic
9 € Allows for search of Euro Basic
10 in Allows searches for unit conversion (currency, unit or
measure)
Basic
11 ~ Prefix - Include synonyms (potentially defunct) Basic
12 + Prefix - Force exact match on single phrase Basic, Mail
13 daterange: Return results in a specified range (requires julian
dates)
Advanced
14 link: Find pages that link to the target domain Advanced
15 inanchor: Find pages linked to with the specified anchor text/
phrase. Data is heavily sampled.
Advanced
16 allinanchor: Find pages with all individual terms after "inanchor:"
in the inbound anchor text.
Advanced
17 inposttile: Finds pages with keywords in their post titles
(i.e. for researching blogs)
18 define: Pulls a card response from Google displaying
the dictionary definition of the word or phrase
Advanced
19 cache: Returns the most up to date cache of an indexed web
page
Advanced
20 filetype: Returns only files of a particular type associated with
the keyword searched
Advanced
21 ext: As above, based on extension Advanced
22 site: Limit results to those from one site Advanced
23 related: Find similar domains to the queried domain Advanced
24 intitle: Returns pages based on the searched query appearing
in their title
Advanced
25 allintitle: Similar to intitle: but only returns titles where all
the words in the title match
Advanced
26 inurl: Only returns results where the queried keyword(s) is
present in the URL
Advanced
27 allinurl: As above but only containing all of the specified words
in the URL
Advanced
28 intext: Finds pages where the keyword(s) are mentioned
within the page content.
Advanced
29 allintext: Similar to “intext,” but only results containing all
of the specified words somewhere on the page will be
returned.
Advanced
30 AROUND(X) This is sandwiched between two words and the X
declares how many words they must be mentioned
between. I.e. if it’s (4) then the two keywords must be
mentioned within 4 words of each other.
Advanced
31 weather: Brings up the featured snipped for weather
for that location
Advanced
32 stocks: Returns stock information for the specified ticker Advanced
33 map: Force google map results for a particular query Advanced
34 movie: Find information for the specified movie (particularly
useful when that movie has an ambiguous name).
If the movie is still in theatres it’ll also return screen
times
Advance
35 source: Use in google news, returns results from
the specified source
Advanced
36 _ Acts as wildcard for autocomplete Advanced
37 blogurl: Find blog URLs under a specific domain. This was
used in Google blog search, but I’ve found it does
return some results in regular search.
Advanced
38 loc: Returns results for a specific location Advanced
39 location: As above but with Google news Advanced
40 info: Returns information rlated to a domain (pages with
dmain text, similar on-site pages, cache etc)
Advanced
41 near Part of the google maps lazy searches e.g. book
shops near work
Maps
42 Business type E.g. cafe, restaurant, bar etc will return a selection
of appropriate businesses in the are
Maps
43 Petrol/Charging
Station
EV near me or perol station near me returns Maps
44 type: Allows you to search drive by file type Drive
45 owner: Allows you to search drive by owner of file
or folder
Drive
46 after: Allows you to search drive or mail for files modified or
mail sent/received anytime after a set date
Drive, Mail
47 before: Allows you to search drive or mail for files modified or
mail sent/received before
a certain date
Drive, Mail
48 to: Allows you to search drive for files shared with
a specific person
Drive
49 title: Searches drive for files with the keyword
in their title alone
Drive
50 source:domain Allows you to search for files or folders shared with
everyone in your business
Drive
51 is:trashed Searches for the item in the Drive bin Drive
52 is:starred Searches only items that have been starred
in drive
Drive, Mail
53 from: Specify the sender in google mail Mail
54 to: Specify the recipient in google mail Mail
55 cc: Search by a recipient that was copied into
an email
Mail
56 bcc: Search by a recipient that was blind copied into
an email
Mail
57 subject: Search by keywords featured in the subject line Mail
58 {} Use for OR in mail instead of the OR function Mail
59 AROUND Similar to the normal google search function, allows
you to search for keywords near each other.
Mail
60 label: Search for messages that have a certain label Mail
61 has:attachment Search for messages that have an item attached Mail
62 has:drive Search for messages with a google drive attached Mail
63 has:document Search for messages with a google doc attached Mail
64 Search for a message with a google sheet attached Mail
65 Search for a message with a google presentation
attached
Mail
66 has:youtube Search for a message containing a youtube video Mail
67 list: Search for all messages from a particular mailing list Mail
68 filename: Search for messages with a particular type of file
attached, or the exact name of a file
Mail
69 in:anywhere Includes all folders in your search, including spam and
bin
Mail
70 is:important Search for messages that have been marked as
important
Mail
71 label:important Same as is:important Mail
72 is:snoozed Searches for messages that have been snoozed Mail
73 is:unread Searches for unread messages Mail
74 is:read searches for read messages only Mail
75 has:yellow-star Searches for messages with coloured star icon Mail
76 has:blue-info Searches for messages with colourd icon Mail
77 older: Search for messages older than a certain date Mail
78 newer: Search for messages newer than a certain date Mail
79 is:chat Searches for messagse from chat Mail
80 deliveredto: Search by email address for delivered messages Mail
81 category: Searches by messages based on category. Follow
the colon with the categoy name, i.e. category:primary
Mail
82 size: Messages larger than a certain size in bytes Mail
83 larger: Messages larger than a certain size in bytes Mail
84 smaller: Messages smaller than a certain size in bytes Mail
85 has:userlabels Search for messages that have custom user labels Mail


Transform this google search prompt into quality one:
Example: Give me articles on EU AI Act that were published after 21.05.2023
