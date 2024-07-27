import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count, Q, Avg
from main_app.models import Author, Article


def get_authors(search_name=None, search_email=None):
    if search_email is None and search_name is None:
        return ''

    elif search_email is None:
        query = Q(full_name__icontains=search_name)

    elif search_name is None:
        query = Q(email__icontains=search_email)

    else:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ''

    return "\n".join([f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"
                      for a in authors])


def get_top_publisher():
    top_publisher = Author.objects.get_authors_by_article_count().filter(article_count__gt=0).first()

    if not top_publisher:
        return ''

    return f"Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles."


def get_top_reviewer():

    top_reviewer = Author.objects.annotate(
        review_count=Count('review')
    ).filter(review_count__gt=0
             ).order_by('-review_count', 'email').first()

    if not top_reviewer:
        return ''

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews."


def  get_latest_article():
    article = Article.objects.prefetch_related('authors', 'review_set__author').order_by('-published_on').first()

    if not article:
        return ''

    authors = ', '.join(a.full_name for a in article.authors.order_by('full_name'))
    review_count = article.review_set.count()
    avg_rating = sum(r.rating for r in article.review_set.all())/ review_count if review_count else 0.0

    return (f"The latest article is: {article.title}. Authors: {authors}. Reviewed: {review_count} times. "
            f"Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    top_rated_art = Article.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating', 'title').first()
    rating_count = top_rated_art.review_set.count() if top_rated_art else 0
    if top_rated_art is None or rating_count == 0:
        return ''
    avg_rating = top_rated_art.avg_rating or 0.0
    return (f"The top-rated article is: {top_rated_art.title}, with an average rating of "
            f"{avg_rating:.2f}, reviewed {rating_count} times.")


def ban_author(email=None):
    author = Author.objects.prefetch_related('reviews').filter(email__exact=email).first()

    if email is None or not author:
        return "No authors banned."

    review_count = author.reviews.count()

    author.is_banned = True
    author.save()

    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {review_count} reviews deleted."


