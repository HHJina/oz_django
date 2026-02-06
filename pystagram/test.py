from django.db import connection

from apps.blog.models import Post

# django ORM "Lazy Loading"
# Eager loading
posts = Post.objects.all().select_related(
    "author",
    "category",
)

for post in posts:
    print(post.id)
    print(post.title)
    print(post.author)  # User object
    print(post.category)  # Category object
    print("====================")

print("총 쿼리 개수 >> ", len(connection.queries))

for sql in connection.queries:
    print(sql["sql"])