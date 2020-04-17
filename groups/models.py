from django.db import models
from django.utils.text import slugify
# Create your models here.
import misaka
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse


class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True,blank=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        self.description_html=misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering=['name']

class GroupMember(models.Model):
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)
    group = models.ForeignKey(Group,related_name='memberships', on_delete=models.CASCADE)
    name = models.CharField(blank=True,null=True,max_length=256)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together=('group','user')



