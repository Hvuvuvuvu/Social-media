from django.db import models
from django.conf import settings

class Publication(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='publications'
    )
    publicate_date = models.DateTimeField()


class Comment(models.Model):
    answer = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media_file = models.FileField(upload_to="comment_media/", blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.creator} on {self.answer}"