from blog.models import Category, Post


def create_politics_category():
    return Category.objects.create(
        name='Politics'
    )


def create_post(user, category):
    return Post.objects.create(
        title='test_title',
        category=category,
        content='test_content',
        author=user
    )
