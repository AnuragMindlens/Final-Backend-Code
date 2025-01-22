from django.db import models


class Images(models.Model):
    """Image response metadata

    Args:
        models (Model): db model

    Returns:
        Charfield: title character field
    """
    title = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
