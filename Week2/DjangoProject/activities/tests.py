from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import ActivityForm
from .models import Activity


class ActivityFormTests(TestCase):
    def test_reject_start_time_in_past(self):
        past = timezone.localtime() - timedelta(minutes=5)
        form = ActivityForm(data={
            'title': '过期活动',
            'start_time': past.strftime('%Y-%m-%dT%H:%M'),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('start_time', form.errors)
        self.assertIn('开始时间不能早于当前时间', form.errors['start_time'][0])

    def test_accept_start_time_in_future(self):
        future = timezone.localtime() + timedelta(days=1)
        form = ActivityForm(data={
            'title': '新活动',
            'start_time': future.strftime('%Y-%m-%dT%H:%M'),
        })
        self.assertTrue(form.is_valid())


class ActivityViewTests(TestCase):
    def setUp(self):
        self.future = timezone.localtime() + timedelta(days=3)
        self.party = Activity.objects.create(
            title='联欢会',
            start_time=self.future,
            location='xjcc',
            description='吃xjcc',
        )
        self.meeting = Activity.objects.create(
            title='爱特例会',
            start_time=self.future + timedelta(days=1),
            location='58工坊',
            description='111',
        )

    def test_search_filters_by_title(self):
        response = self.client.get(reverse('activities:activity_list'), {'q': '联欢'})
        self.assertContains(response, '联欢会')
        self.assertNotContains(response, '爱特例会')
        self.assertEqual(list(response.context['activities']), [self.party])

    def test_empty_keyword_shows_all(self):
        response = self.client.get(reverse('activities:activity_list'), {'q': '  '})
        self.assertEqual(response.context['activities'].count(), 2)

    def test_create_view(self):
        future = (timezone.localtime() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(reverse('activities:activity_create'), {
            'title': '招新宣讲',
            'start_time': future,
            'location': '教学楼',
            'description': '介绍社团',
        })
        self.assertRedirects(response, reverse('activities:activity_list'))
        self.assertTrue(Activity.objects.filter(title='招新宣讲').exists())

    def test_update_view_reuses_form(self):
        response = self.client.get(reverse('activities:activity_update', args=[self.party.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ActivityForm)
        self.assertEqual(response.context['form'].instance, self.party)

        new_time = (timezone.localtime() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(
            reverse('activities:activity_update', args=[self.party.pk]),
            {
                'title': '联欢会（改期）',
                'start_time': new_time,
                'location': 'xjcc',
                'description': '吃xjcc',
            },
        )
        self.assertRedirects(response, reverse('activities:activity_list'))
        self.party.refresh_from_db()
        self.assertEqual(self.party.title, '联欢会（改期）')

    def test_update_rejects_past_start_time(self):
        past = (timezone.localtime() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(
            reverse('activities:activity_update', args=[self.party.pk]),
            {
                'title': '联欢会',
                'start_time': past,
                'location': 'xjcc',
                'description': '吃xjcc',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '开始时间不能早于当前时间')
        self.party.refresh_from_db()
        self.assertEqual(self.party.title, '联欢会')

    def test_delete_page_asks_for_confirmation(self):
        response = self.client.get(reverse('activities:activity_delete', args=[self.party.pk]))
        self.assertContains(response, '确认删除')
        self.assertTrue(Activity.objects.filter(pk=self.party.pk).exists())

    def test_delete_view(self):
        response = self.client.post(reverse('activities:activity_delete', args=[self.party.pk]))
        self.assertRedirects(response, reverse('activities:activity_list'))
        self.assertFalse(Activity.objects.filter(pk=self.party.pk).exists())
