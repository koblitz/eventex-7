# coding: utf-8
from django.db import IntegrityError
from django.test import TestCase
from ..models import Subscription


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
