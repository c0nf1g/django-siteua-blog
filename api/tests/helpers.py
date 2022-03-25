from blog.models import Category, Post, Comment


def create_categories():
    categories_names = ['Politics', 'Sport', 'Economics']
    categories = []

    for name in categories_names:
        categories.append(Category.objects.create(
            name=name
        ))

    return categories


def create_posts(user):
    categories = create_categories()
    posts = []

    for category in categories:
        posts.append(
            Post.objects.create(
                title='test title',
                category=category,
                content='test content',
                author=user
            )
        )

    return posts


def create_comments(user):
    posts = create_posts(user)
    comments = []

    for post in posts:
        comments.append(
            Comment.objects.create(
                content='test comment',
                author=user,
                post=post
            )
        )

    return comments
