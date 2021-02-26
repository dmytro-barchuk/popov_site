from django.db import models
from pytils.translit import slugify
from sorl.thumbnail import ImageField
from datetime import datetime


class Tag(models.Model):
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name


class Post(models.Model):
	title = models.CharField(max_length=100, verbose_name = "Заголовок")
	image = models.ImageField(verbose_name = "Малюнок або фото:", null=True, blank=True, upload_to="images/%Y/%M/", default="/no_image.png")
	body = models.TextField(verbose_name ="Опис (не обов'язково):", null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	tags = models.ManyToManyField(Tag, null=True, verbose_name ="Теги:",)
	slug = models.SlugField(max_length=120, null = True, blank=True, verbose_name ="Slug (не заповнювати): ")


	def __str__(self):
		return self.title


	def save(self, *args, **kwargs):

		if self.slug == None:
			slug = slugify(self.title)

			has_slug = Post.objects.filter(slug=slug).exists()
			count = 1
			while has_slug:
				count += 1
				slug = slugify(self.title) + '-' + str(count) 
				has_slug = Post.objects.filter(slug=slug).exists()

			self.slug = slug

		super(Post, self).save(*args, **kwargs)