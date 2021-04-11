from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context['header'] = 'Об авторе'
        context['preface'] = 'Краткая информация'
        context['text'] = (
            'Здесь должна быть какая-то информация об авторе '
            'данного творения. Однажды она появится, '
            'но не сегодня.'
        )
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['header'] = 'Технологии'
        context['preface'] = 'шагнули очень далеко вперёд.'
        context['text'] = (
            'Речь пойдёт об интернете. '
            'Кто не понял, тот поймёт.'
        )
        return context
