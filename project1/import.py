import os, csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not scet")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open('books.csv')
    reader = csv.reader(f)
    next(reader) #to reject header
    for isbh, title, author, year in reader:
        print(isbh, title, author, year)
        db.execute("INSERT INTO books (isbh, title, author, year) VALUES (:isbh, :title, :author, :year)",
                    {"isbh": isbh, "title": title, "author": author, "year": year})
    db.commit()
if __name__ == '__main__':
    main()
