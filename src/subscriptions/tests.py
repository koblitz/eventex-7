# coding: utf-8
from django.db import IntegrityError
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Subscription
from .forms import SubscriptionForm


class SubscriptionUrlTest(TestCase):
    def test_get_subscribe_page(self):
        response = self.client.get(reverse('subscriptions:subscribe'))
        self.assertEquals(200, response.status_code)

    def test_get_success_page(self):
        response = self.client.get(reverse('subscriptions:success', args=[1]))
        self.assertEquals(200, response.status_code)


class SubscriptionModelTest(TestCase):
    def test_create(self):
        "O modelo deve ter os campos: name, cpf, email, phone, created_at."

        s = Subscription.objects.create(
            name='Henrique Bastos',
            cpf='012345678901',
            email='henrique@bastos.net',
            phone='21-96186180'
        )
        self.assertEquals(s.id, 1)


class SubscriptionModelUniqueTest(TestCase):
    def setUp(self):
        "Cria uma primeira inscrição no banco."
        Subscription.objects.create(name='Henrique Bastos', cpf='012345678901',
                                    email='henrique@bastos.net', phone='21-96186180')

    def test_cpf_must_be_unique(self):
        "O cpf deve ser único."

        # Instancia a inscrição com CPF existente
        s = Subscription(name='Henrique Bastos', cpf='012345678901',
                         email='outro@email.com', phone='21-96186180')
        # Verifica se ocorre o erro de integridade ao persistir.
        self.assertRaises(IntegrityError, s.save)

    def test_email_must_be_unique(self):
        "O email deve ser único."

        # Instancia a inscrição com Email existente
        s = Subscription(name='Henrique Bastos', cpf='00000000000',
                         email='henrique@bastos.net', phone='21-96186180')
        # Verifica se ocorre o erro de integridade ao persistir.
        self.assertRaises(IntegrityError, s.save)


class SubscribeViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('subscriptions:subscribe'))

    def test_get(self):
        "Ao visitar /inscricao/ a página de inscrição é exibida."
        self.assertEquals(200, self.resp.status_code)

    def test_use_template(self):
        "O corpo da resposta deve conter a renderização de um template."
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        "A resposta deve conter o formulário de inscrição"
        self.assertIsInstance(self.resp.context['form'], SubscriptionForm)

    def test_form_has_fields(self):
        "O formulário de deve conter campos: name, email, cpf e phone."
        form = self.resp.context['form']
        self.assertItemsEqual(['name', 'email', 'cpf', 'phone'], form.fields)

    def test_html(self):
        "O html deve conter os campos do formulário"
        self.assertContains(self.resp, 'form')
        self.assertContains(self.resp, 'input', 6)
        self.assertContains(self.resp, 'type="text"', 4)
        self.assertContains(self.resp, 'submit')


class SubscribeViewPostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='00000000000',
                    email='henrique@bastos.net', phone='21-96186180')
        self.resp = self.client.post(reverse('subscriptions:subscribe'), data)

    def test_post(self):
        "Post deve redirecionar para página de sucesso."
        self.assertRedirects(self.resp,
                             reverse('subscriptions:success', args=[1]))

    def test_save(self):
        "Post deve salvar Subscription no banco."
        self.assertTrue(Subscription.objects.exists())


class SubscribeViewInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='000000000001',
                    email='henrique@bastos.net', phone='21-96186180')
        self.resp = self.client.post(reverse('subscriptions:subscribe'), data)

    def test_show_page(self):
        "Post inválido não deve redirecionar."
        self.assertEqual(200, self.resp.status_code)

    def test_form_errors(self):
        "Form deve conter erros."
        self.assertTrue(self.resp.context['form'].errors)

    def test_must_not_save(self):
        "Dados não devem ser salvos."
        self.assertFalse(Subscription.objects.exists())

