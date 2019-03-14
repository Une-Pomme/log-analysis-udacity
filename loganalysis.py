#!/usr/bin/env python
#
# file: loganalysis.py
# author: Lianne McIntosh

import psycopg2


def get_three_top_articles():
    db = psycopg2.connect("dbname=news")
    curr = db.cursor()
    query = """
        select title, count(*) as views
        from articles, log
        where log.path like '%'||articles.slug||'%'
        group by articles.id
        order by views desc
        limit 3;
        """
    curr.execute(query)
    rows = curr.fetchall()
    db.close()
    return rows


def get_most_popular_authors():
    db = psycopg2.connect("dbname=news")
    curr = db.cursor()
    query = """
        select name, count(*) as views
        from articles, log, authors
        where (log.path like '%'||articles.slug||'%'
        and articles.author=authors.id)
        group by authors.name
        order by views desc;
    """
    curr.execute(query)
    rows = curr.fetchall()
    db.close()
    return rows


def more_than_one_percent_errors():
    db = psycopg2.connect("dbname=news")
    curr = db.cursor()
    query = """
        select subq.date,
        floor((subq.errors*1.0/subq2.all_statuses) * 100) as rate
        from (select date(time) as date,
        count( case when status like '4%'
        or status like '5%' then 1 else null end) as errors
        from log
        group by date(time) ) as subq join
        (select date(time) as date,
        count(*) as all_statuses
        from log
        group by date(time)) as subq2
        on subq.date = subq2.date
        where (subq.errors*1.0/subq2.all_statuses) > .01;
    """
    curr.execute(query)
    rows = curr.fetchall()
    db.close()
    return rows


def main():
    top_articles = get_three_top_articles()
    print "\nMost popular three articles of all time:"
    for article in top_articles:
        print '"'+article[0]+'" --', article[1], 'views'
    most_popular_authors = get_most_popular_authors()
    print "\nMost popular article authors of all time:"
    for author in most_popular_authors:
        print author[0], "--", author[1], "views"
    days_with_errors = more_than_one_percent_errors()
    print "\nDays where more than 1% of requests lead to errors:"
    for day in days_with_errors:
        print day[0], "--", str(day[1])+"%", "errors"


main()
