# Log Analysis

My submission for the log analysis project was written with Python 2. I included an output text file.

## Usage
```
python loganalysis.py
```

## Design

The loganalysis.py file connects to the news database and answers three questions: 1) What are the three most popular articles, 2) Who are the most popular authors, and 3) Which days had more than 1% of the requests lead to errors. Each question is printed out and the results are given below the question.

The first question utilizes a query that joins the articles table and the log table in order to count how many views each article recieved.

The query in the second question finds out the number of total views an author recieved based on the articles they have written. This joins the articles, log and authors tables.

The third query uses two subqueries and joins the results to answer the question. The first subquery looks at the log table and counts the number of times per day that a 4xx or 5xx error status was recorded. The second subquery looks at the log table and counts how many times per day any status was recorded.

## Author

Lianne McIntosh