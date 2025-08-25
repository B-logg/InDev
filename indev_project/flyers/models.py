from django.db import models

class Flyer(models.Model):
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True, default="")
    width = models.PositiveIntegerField(default=768)
    height = models.PositiveIntegerField(default=1024)
    steps = models.PositiveIntegerField(default=30)
    guidance_scale = models.FloatField(default=7.5)
    seed = models.BigIntegerField()
    image = models.ImageField(upload_to="flyers/%Y/%m/%d/")  # MEDIA_ROOT 하위 경로
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.prompt[:30]}..."
