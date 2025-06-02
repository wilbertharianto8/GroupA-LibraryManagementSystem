# Export Groups
python manage.py dumpdata auth.Group \
  --natural-primary \
  --natural-foreign \
  --indent=2 \
  > fixtures/groups.json

# Export Users (reference groups by name)
python manage.py dumpdata auth.User \
  --indent=2 \
  --natural-primary \
  --natural-foreign \
  > fixtures/users.json

# Export Books
python manage.py dumpdata books.Book \
  --indent=2 \
  --natural-primary \
  --natural-foreign \
  > fixtures/books.json

# Export Genres
python manage.py dumpdata books.Genre \
  --indent=2 \
  --natural-primary \
  --natural-foreign \
  > fixtures/genre.json