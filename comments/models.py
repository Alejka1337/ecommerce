from django.db import models
from django.conf import settings
from ecomm.models import Product


class Comment(models.Model):

    product = models.ForeignKey(
        Product,
        verbose_name="product",
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )
    message = models.TextField("comment", db_index=True)
    name = models.CharField("name", max_length=50, null=True, blank=True)
    email = models.CharField("email", max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return self.message[:50]

