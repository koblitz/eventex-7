# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Speaker
from .models import Contact
from .models import Talk
from .models import PeriodManager


class HomepageTest(TestCase):
    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')


class SpeakerModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker(name="Henrique Bastos",
                               slug="henrique-bastos",
                               url="http://henriquebastos.net",
                               description="Passionate software developer!",
                               avatar="")
        self.speaker.save()

    def test_create(self):
        self.assertEqual(1, self.speaker.pk)

    def test_unicode(self):
        self.assertEqual(u"Henrique Bastos", unicode(self.speaker))


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(name="Henrique Bastos",
                                              slug="henrique-bastos",
                                              url="http://henriquebastos.net",
                                              description="Passionate software developer!",
                                              avatar="")
    def test_create_email(self):
        contact = Contact.objects.create(speaker=self.speaker, kind='E', value='henrique@bastos.net')
        self.assertEqual(1, contact.pk)

    def test_create_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind='P', value='21-96186180')
        self.assertEqual(1, contact.pk)

    def test_create_fax(self):
        contact = Contact.objects.create(speaker=self.speaker, kind='F', value='21-98989898')
        self.assertEqual(1, contact.pk)


class TalkModelTest(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(
            title=u'Introdução ao Django',
            description=u'Descrição da Palestra',
            start_time='10:00')

    def test_create(self):
        self.assertEqual(1, self.talk.pk)

    def test_unicode(self):
        self.assertEqual(u'Introdução ao Django', unicode(self.talk))

    def test_period_manager(self):
        self.assertIsInstance(Talk.objects, PeriodManager)


class PeriodManagerTest(TestCase):
    def setUp(self):
        Talk.objects.create(title=u'Morning Talk', start_time='10:00')
        Talk.objects.create(title=u'Afternoon Talk', start_time='12:00')

    def test_morning(self):
        self.assertQuerysetEqual(Talk.objects.at_morning(), ['Morning Talk'], lambda t: t.title)

    def test_afternoon(self):
        self.assertQuerysetEqual(Talk.objects.at_afternoon(), ['Afternoon Talk'], lambda t: t.title)


class SpeakerDetailTest(TestCase):
    def setUp(self):
        Speaker.objects.create(name="Henrique Bastos",
                               slug="henrique-bastos",
                               url="http://henriquebastos.net",
                               description="Passionate software developer!",
                               avatar="")
        self.resp = self.client.get(reverse('core:speaker_detail', kwargs={'slug': 'henrique-bastos'}))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/speaker_detail.html')

    def test_speaker_in_context(self):
        speaker = self.resp.context['speaker']
        self.assertIsInstance(speaker, Speaker)


class TalksViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('core:talks'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/talks.html')

    def test_morning_talks_in_context(self):
        self.assertIn('morning_talks', self.resp.context)

    def test_afternoon_talks_in_context(self):
        self.assertIn('afternoon_talks', self.resp.context)
