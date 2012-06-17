# coding: utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.views.generic import DetailView

from src.core.models import Speaker
from src.core.models import Talk

class Homepage(TemplateView):
    template_name='index.html'


class SpeakerDetail(DetailView):
    model = Speaker


def talks(request):
    context = {
        'morning_talks': Talk.objects.at_morning(),
        'afternoon_talks': Talk.objects.at_afternoon(),
    }
    return direct_to_template(request, 'core/talks.html', context)


class TalkDetail(DetailView):
    model = Talk
