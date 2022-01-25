"""Audio book product models."""
# from base.models import Base
from django.db import models
from django.conf import settings
from account.models import User
from base.models import BaseComment, BaseStar

from base.models import (
    Translator,
    Author,
    Publisher,
    # Speaker,
    # BaseInventory,
)
from .product import Product


class PaperBook(Product):
    """Paper book product model."""

    intro = models.URLField()
    # description = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    # speakers = models.ManyToManyField(Speaker)
    translators = models.ManyToManyField(Translator)
    # authors = models.ManyToManyField(Author, related_name="audio_book_author")
    # speakers = models.ManyToManyField(Speaker, related_name="audio_book_speaker")
    # translators = models.ManyToManyField(Translator, related_name="audio_book_translator")
    book_publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="paper_book_publisher"
    )
    # audio_publisher = models.ForeignKey(
    #     Publisher, on_delete=models.CASCADE, related_name="audio_publisher"
    # )
    # bookmarks = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL, related_name="paper_book_bookmarks"
    # )
    # indices = models.ForeignKey(AudioIndex, on_delete=models.DO_NOTHING)
    published_year = models.PositiveSmallIntegerField()
    # audio_type = models.ForeignKey(AudioType, on_delete=models.DO_NOTHING)
    # compatible_devices = models.ManyToManyField(CompatibleDevice)
    # is_downloadable = models.BooleanField(default=False)


# class PaperBookInventory(BaseInventory):
#     product = models.ForeignKey(
#         PaperBook,
#         on_delete=models.CASCADE,
#         related_name='inventory_set',
#     )
#
#     quantity = models.PositiveIntegerField(
#         # _("Quantity"),
#         default=0,
#         # validators=[MinValueValidator(0)],
#         # help_text=_("Available quantity in stock")
#     )


class PaperBookComment(BaseComment):
    """Comment model implementation."""

    user = models.ForeignKey(
        User, related_name="paper_book_comment_user", on_delete=models.CASCADE
    )
    # message = models.CharField(max_length=500)
    # reply_to = models.ForeignKey(
    #     "self", on_delete=models.CASCADE, null=True, default=""
    # )
    Product = models.ForeignKey(PaperBook, related_name="paper_book_comments", on_delete=models.CASCADE)
    # is_approved = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ["created_at"]

    # def __str__(self):
    #     if self.is_deleted:
    #         return f"{self.message} [deleted]"
    #     return self.message


# class PostStar(AbstractBase):
class PaperBookStar(BaseStar):
    """Star (posts) model implementation."""

    # star = models.PositiveSmallIntegerField(
    #     validators=[
    #         MinValueValidator(settings.STAR_MIN_VALUE),
    #         MaxValueValidator(settings.STAR_MAX_VALUE),
    #     ]
    # )
    user = models.ForeignKey(User, related_name="paper_book_star_user", on_delete=models.CASCADE)
    product = models.ForeignKey(PaperBook, related_name="paper_book_stars", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
        unique_together = [("user", "product")]

    def __str__(self):
        return f"{self.post.title}[{self.star}]"
