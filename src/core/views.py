from django.views.generic import TemplateView, ListView

from subscriptions.models import Subscription, Basic, Premium, Enterprise
from .models import Books
from django.shortcuts import render

from common.mixins import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name: str = "partials/index.html"
    title: str = "Home"

    # @staticmethod
    # def get_search_results(query, correction: bool = False, size: int = 5):
    #     query = query.lower()
    #     search_query = Q(
    #         "bool",
    #         should=[
    #             Q("multi_match", query=query, fields=['title^7', 'author^2', 'description'],
    #               fuzziness='AUTO', prefix_length=2, operator='and'),
    #             Q("wildcard", title={"value": f"*{query}*", "boost": 7}),
    #             Q("wildcard", author={"value": f"*{query}*", "boost": 2}),
    #             Q("wildcard", description={"value": f"*{query}*"}),
    #         ],
    #         minimum_should_match=1
    #     )
    #     search = BookDocument.search().query(search_query)[0:size if correction else None]
    #     results = [hit.to_dict() for hit in search]
    #     return results
    #
    # @staticmethod
    # def get_correction_query(query):
    #     suggest = Search(index="books")
    #     for field in ['title', 'author', 'description']:
    #         suggest = suggest.suggest(f'{field}_suggestion', query, term={'field': field})
    #     response = suggest.execute()
    #
    #     best_correction = query
    #     for suggestion in response.suggest:
    #         if response.suggest[suggestion][0].options:
    #             best_correction = response.suggest[suggestion][0].options[0].text
    #             break
    #     return best_correction if best_correction != query else None
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     query = self.request.GET.get('q')
    #     if query:
    #         context['original_query'] = query
    #         books = self.get_search_results(query)
    #         correction = self.get_correction_query(query)
    #         if correction and correction.lower() != query.lower():
    #             context['correction'] = correction
    #             corrected_books = self.get_search_results(correction)
    #             if corrected_books:
    #                 context['books'] = corrected_books
    #             else:
    #                 context['books'] = books
    #         else:
    #             context['books'] = books
    #             context['correction'] = None
    #     else:
    #         search = Search(index="books")
    #         response = search.scan()
    #         context['books'] = [hit.to_dict() for hit in response]
    #         context['correction'] = None
    #     return context
    #
    # def get(self, request, *args, **kwargs):
    #     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #         query = request.GET.get('q', '')
    #         suggestions = self.get_search_results(query, correction=True) if query else []
    #         if not suggestions:
    #             correction = self.get_correction_query(query)
    #             if correction and correction.lower() != query.lower():
    #                 suggestions = self.get_search_results(correction, correction=True)
    #                 suggestions.append({'correction': correction, 'original_query': query})
    #         return JsonResponse(suggestions, safe=False)
    #     return super().get(request, *args, **kwargs)


class BookList(TitleMixin, ListView):
    template_name: str = "partials/books_list.html"
    title: str = "Books"
    model = Books
    context_object_name: str = 'books'
    ordering = ['title']


def subscription_plans(request):
    basic_plan = Basic.objects.first()
    premium_plan = Premium.objects.first()
    enterprise_plan = Enterprise.objects.first()
    try:
        subscriptions = Subscription.objects.get(user=request.user)
        subscription_id = subscriptions.paypal_subscription_id
        subscription_plan = subscriptions.subscription_plan
        context = {'subscription_plan': subscription_plan, 'subscription_id': subscription_id,
                   'basic_plan': basic_plan, 'premium_plan': premium_plan, 'enterprise_plan': enterprise_plan}
    except:
        context = {'subscription_plan': None, 'subscription_id': None, 'basic_plan': basic_plan,
                   'premium_plan': premium_plan, 'enterprise_plan': enterprise_plan}

    return render(request, 'partials/pricing.html', context)


class Handler403(TitleMixin, TemplateView):
    template_name: str = '403.html'
    title: str = '403 Forbidden'


class Handler404(TitleMixin, TemplateView):
    template_name = '404.html'
    title: str = '404 Not Found'


class Handler500(TitleMixin, TemplateView):
    template_name: str = '500.html'
    title: str = '500 Internal Server Error'

class Handler502(TitleMixin, TemplateView):
    template_name: str = '502.html'
    title: str = '502 Bad Gateway'


class Handler503(TitleMixin, TemplateView):
    template_name: str = '503.html'
    title: str = '503 Service Unavailable'


