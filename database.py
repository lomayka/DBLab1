import psycopg2
import random_generator
import random

connect = psycopg2.connect("host=localhost dbname=library user=postgres password=123")

cursor = connect.cursor()


def insert_reader(name, registration_date):
    insert = "INSERT INTO Readers VALUES {}".format("(\'" + name + '\',\'' + registration_date + "\')")

    cursor.execute(insert)
    connect.commit()


def insert_book(name, annotation):
    insert = "INSERT INTO Books VALUES {}".format("(\'" + name + '\',\'' + annotation + "\')")

    cursor.execute(insert)
    connect.commit()


def insert_author(name, date_of_birth, book_id):
    cursor.execute("SELECT * FROM Books WHERE id = \'" + book_id + "\'")
    if cursor.fetchall is not []:
        insert = "INSERT INTO Authors (name, birthdate) VALUES (%s, %s) RETURNING id"

        cursor.execute(insert, (name, date_of_birth))
        author = cursor.fetchone()[0]
        insert = "INSERT INTO Written (author, bookid) VALUES (%s, %s)"
        cursor.execute(insert, (author, book_id))
        connect.commit()
    else:
        raise Exception("No book with such id")


def delete_reader(readerid):
    cursor.execute('DELETE FROM Readers WHERE id = ' + readerid)
    cursor.execute('DELETE FROM Taken WHERE readerid = ' + readerid)


def delete_book(bookid):
    cursor.execute('DELETE FROM Books WHERE id = ' + bookid)
    cursor.execute('DELETE FROM Written WHERE bookid = ' + bookid)
    cursor.execute('DELETE FROM Taken WHERE bookid = ' + bookid)


def delete_author(authorid):
    cursor.execute('DELETE FROM Authors WHERE id = ' + authorid)
    cursor.execute('DELETE FROM Written WHERE authorid = ' + authorid)


def insert_random_reader():
    insert_reader(random_generator.random_name(), random_generator.random_date("1980-01-01", "2018-01-01"))


def insert_random_author():
    insert = "INSERT INTO Authors (name, birthdate) VALUES (%s, %s) RETURNING id"

    cursor.execute(insert, (random_generator.random_name(), random_generator.random_date("1750-01-01", "2018-01-01")))
    author = cursor.fetchone()[0]
    insert = "INSERT INTO Written (authorid, bookid) VALUES (%s, %s)"
    cursor.execute('SELECT Id FROM Books')
    ids = cursor.fetchall()
    cursor.execute(insert, (author, random.choice(ids)))
    connect.commit()


def insert_random_book():
    insert_book(random_generator.random_book_name(), random_generator.random_text())


def fetch_readers():
    cursor.execute('SELECT * FROM Readers')
    return cursor.fetchall()


def fetch_books():
    cursor.execute('SELECT * FROM Books')
    return cursor.fetchall()


def fetch_authors():
    cursor.execute('SELECT * FROM Authors')
    return cursor.fetchall()


def find_reader_by_name(name):
    cursor.execute('SELECT * FROM Readers WHERE \"ReaderName\" = \'' + name + '\'')
    return cursor.fetchone()


def find_books_by_author_date(first_date, last_date):
    sql = """
        SELECT books.name, authors.name, authors.birthdate
          FROM books
        LEFT OUTER JOIN written
          ON books.id = written.bookid
        LEFT OUTER JOIN authors
          ON written.authorid = authors.id
         WHERE birthdate >= %s AND birthdate <= %s"""
    cursor.execute(sql, (first_date, last_date))
    return cursor.fetchall()


def find_readers_by_annotation(phrase):
    sql = """
        SELECT books.name, books.annotation, readers.name
          FROM books
        LEFT OUTER JOIN taken
          ON books.id = taken.bookid
        LEFT OUTER JOIN readers
          ON taken.readerid = readers.id
        WHERE to_tsvector(books.annotation) @@ phraseto_tsquery('%s')""" % phrase
    cursor.execute(sql)
    return cursor.fetchall()


def find_authors_by_part_name(word):
    sql = """
    SELECT * FROM Authors
        WHERE NOT to_tsvector(authors.name) @@ to_tsquery('%s')""" % word
    cursor.execute(sql)
    return cursor.fetchall()


def book_taken_by(reader_id, book_id):
    insert = "INSERT INTO taken VALUES {}".format("(\'" + reader_id + '\',\'' + book_id + "\')")
    cursor.execute(insert)
    connect.commit()


def book_returned_by(reader_id, book_id):
    cursor.execute('DELETE FROM Taken WHERE readerid = ' + reader_id + ' AND bookid = ' + book_id)


def book_written_by(author_id, book_id):
    insert = "INSERT INTO written VALUES {}".format("(\'" + author_id + '\',\'' + book_id + "\')")
    cursor.execute(insert)
    connect.commit()


print(find_readers_by_annotation("Sugarcoating"))


"""
cursor.execute('SELECT Authors."Id" FROM Authors')

listAuthors = cursor.fetchall()

cursor.execute('SELECT Books."Id" FROM Books')

listBooks = cursor.fetchall()

for i in listBooks:
    insert = "INSERT INTO written VALUES {}".format("\'" + i + "" + random.choice(listAuthors))"

print(listAuthors)
print(listBooks)
"""