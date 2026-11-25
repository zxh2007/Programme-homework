from django.db import models


class Activity(models.Model):
    """社团活动"""

    title = models.CharField('标题', max_length=100)
    start_time = models.DateTimeField('开始时间')
    location = models.CharField('地点', max_length=100, blank=True)
    description = models.TextField('活动说明', blank=True)

    class Meta:
        ordering = ['start_time']
        verbose_name = '活动'
        verbose_name_plural = '活动'

    def __str__(self):
        return self.title
