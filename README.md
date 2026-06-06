# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Domain: Best study spots on campus. 

Often times you need a a quiet place to study and get work done. Official websites usually list University libraries or exclusively college facilities. However, University libraries can get very crowded, expecially during exam season. This app will list variety of study spots around campus including cafes/outdoor spots that are within walkable distance from campus. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # |    Source      | Description                    | URL or location |
|---|----------------|--------------------------------|----------------------|
| 1 | HerCampus1.pdf      | Study Spots near GSU       |  ./pdfs/HerCampus1.pdf 
| 2 | StudyNearby.pdf        | Study Spots in GA          |            ./pdfs/StudyNearby.pdf 
| 3 | TheInsightDot.pdf  | Study Spots near GSU           |   ./pdf/sTheInsightDot.pdf
| 4 | HerCampus1.pdf      | Study Spots near GSU           |   ./pdfs/HerCampus1.pdf  
| 5 | Yelp.pdf          | Study Spots near Georgia Tech  |   ./pdf/sYelp.pdf 
| 6 | RamblerAtlanta.pdf | Study Spots near Georgia Tech  |  ./pdfs/RamblerAtlanta.pdf 
| 7 | GaTech.pdf   | Study Spots near Georgia Tech  |  ./pdfs/GATECH.pdf 
| 8 | RedAndBlack.pdf        | Study Spots near UGA |  ./pdfs/RedAndBlack.pdf
| 9 | RamblerAthens.pdf         | Study Spots near UGA  |  ./pdfs/RamblerAthens.pdf
| 10| Odyssey.pdf    | Study Spots near GSU |  ./pdfs/Odyssey.pdf 
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->



**Chunk size:**
400

**Overlap:**
40

**Why these choices fit your documents:**
Most of my documents are pretty structured bulleted text paragraphs. Each around 350-400 characters long. Which is why I used 400 characters chunk size.

**Final chunk count:** 
81. For preprocessing, I copied and pasted the raw text from articles I found online. And removed any white spaces/irrelevant texts etc.


## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 from Sentence Transformers
**Production tradeoff reflection:**
When choosing a model for a production deployment, I would choose a model that has bigger context window and scales better when working with large datasets. 

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The System is instructed to only answer using the context provided.

**How source attribution is surfaced in the response:**
The app lists sources with each response/query. If it can't find a response within the source, it will note it so. For example, I asked something out of scope like study spots near New York University. It returned "There is no information provided about study spots near New York University. The context provided appears to be about study spots on a different campus, possibly Georgia Tech, but it does not mention New York University"

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are some study spots near Georgia Tech that serves coffee or food?| Momo Cafe and Dancing Goats Cafe| Momo Cafe | Partially Relevant | Partially Accurate |
| 2 | What are some study spots near GSU that require a Panther ID to access?| Andrew Young School of Policy Studies| Andrew Young School of Policy Studies| Relevant | Accurate|
| 3 | What are some study spots near Georgia Tech that are open until 10pm?| Momo Cafe and Momokini| Momo Cafe | Partially relevant | Partially accurate |
| 4 | What are some study spots near Georgia Tech that are outdoors? | Roof of Crosland Tower |Tables Near Tech Green | Partially relevant | Partially accurate|
| 5 | What are some study spots near GSU that that are quiet?| Urban Life Building/Courtyard | Urban Life Building|  Relevant| Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
I asked a question about study spots that require a Panther ID. 

**What the system returned:**
Even though it gave the answer correctly, it also suggested College of Law as an option that doesn’t require a Panther ID (Even though it does). 

**Root cause (tied to a specific pipeline stage):**
This was because of insufficient data. Because College of Law doesn’t explicitly mention requiring a Panther ID, it assumed it doesn’t require one. 

**What you would change to fix it:**
I would provide more resources that carries variety of information. I will also instruct the model to not assume things before giving additional responses. 

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
It helped with laying down the step by step process of how to go about creating the pipeline. 

**One way your implementation diverged from the spec, and why:**
However, I had to install some additional packages that are not part of the requirements. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- I directed AI to assist with the generation process, however it listed an older model. And the command line gave me an error, so I revised it to the latest model. 

**Instance 2**

- I also asked AI to list some resources that contained the relevant information that I needed. Even though I ended up using some of its suggestions, I also used some resources that I found online that were more relevant. 

## Sample chunks: at least 5 labeled sample chunks, each with its source document name

Chunk#1: 
Source: TheInsightDot.pdf
Length: 371 chars

Five Best Study Spots at Georgia State University
Andrew Young School of Policy Studies
The Andrew Young School of Policy Studies is one of my favorite places to study. You do not
have to be a student specifically of the Andrew Young School. To get in, all you have to do is
show your panther ID to security. That’s it! There’s a nice lounge area with wide windows that’s

Chunk #2
Source: RamblerAtlanta.pdf
Length: 391 chars

Distance from Rambler: 15-minute drive
Address: 2025 Peachtree Rd NW
Bloom Coffee Co. is a local coffee shop that’s a fifteen-minute drive from campus. This cozy
coffee shop offers unique flavors such as Maple Sea Salt and Island Mocha lattes– the perfect
boost to keep you motivated during your study hour.
If you have any further questions, don’t hesitate to reach out to our leasing team!

Chunk #3
Source: RamblerAtlanta.pdf
Length: 393 chars

Address: 95 8th St NW 100
For a study spot just a few minutes from campus, Momo Cafe is a crowd favorite. Here you can
find Japanese-inspired specialty drinks and pastries for a unique snack to spice up your normal
study session. If you get hungry, the cafe is also attached to a full restaurant with a similar
Japanese-inspired menu, Momonoki.
Caribou Coffee Company
Caribou Coffee in Midtown

Chunk #4
Source: Yelp.pdf
Length: 398 chars

best study spots near Georgia Tech, Atlanta, GA
1. Prevail Union ATL
4.5 (89 reviews)
Westside / Home Park$$Closes in 47 min
"This is a great quiet place to work and study. There's plenty of comfy seating and I feel
like I'm..." more
Coffee Roasteries
2. Momo Cafe
4.3 (271 reviews)
Midtown$Open until 10:00 PM
"This is a great study spot near GT campus! The soft serve was a generous portion and I

Chunk #5
Source: HerCampus1.pdf
Length: 380 chars

Urban Life Building/Courtyard
Urban Life is one of GSU’s older buildings. It has a few floors with lockers and
designated areas for studying. It’s very quiet in the evening which is the perfect time
to look over class notes. If you like to study outside, the Urban Life building has a
courtyard as well that is connected to the GSU Sports Arena.
Third Floor of Student Center East 
