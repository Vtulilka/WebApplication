from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from TransactionsApp.models import Transaction, Category
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Sum, OuterRef, Subquery, F
from .serializers import ReportPeriodSerializer, ReportBudjetSerializer
from BudjetApp.models import Budjet


class ReportViewSet(viewsets.GenericViewSet):
    permission_classes = [ permissions.IsAuthenticated, ]

    def get_queryset(self):
        owner_id = self.request.user.id
        
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if not (start_date and end_date) or start_date > end_date:
            raise serializers.ValidationError('start_date should be less or equal then end_date')
        
        is_expense = 'is_expense' in self.request.GET

        transactions = Transaction.objects.filter(owner_id=owner_id, 
                                                  date__gte=start_date, 
                                                  date__lte=end_date,
                                                  is_expense=is_expense)
        categories = Category.objects.filter(id__in=transactions.values_list('category_id', flat=True),
                                            transactions__is_expense=is_expense,
                                            transactions__date__gte=start_date,
                                            transactions__date__lte=end_date)\
                                    .values('id', 'name')\
                                    .annotate(total_amount=Sum(F('transactions__amount')))
        return [transactions, categories]

    @action(detail=False,
            methods=['get'])
    def period(self, request):
        serializer_class = ReportPeriodSerializer
        transactions, categories = self.get_queryset()
        
        total_amount = transactions.aggregate(s=Sum('amount'))['s']
        owner_id = request.user.id
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        is_expense = 'is_expense' in self.request.GET

        data = request.data
        data['owner_id'] = owner_id
        data['is_expense'] = is_expense
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['total_amount'] = total_amount
        data['transactions'] = transactions
        data['categories'] = categories

        serializer = serializer_class(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['get'])
    def budjet(self, request):
        serializer_class = ReportBudjetSerializer

        budjet_id = self.request.GET.get('budjet_id')
        budjet_obj = Budjet.objects.get(id=budjet_id)
        if not budjet_obj:
            raise serializers.ValidationError('Should specify correct budjet_id')
        
        owner_id = self.request.user.id
        start_date = budjet_obj.start_date
        end_date = budjet_obj.end_date

        transactions = Transaction.objects.filter(owner_id=owner_id,
                                                  date__gte=start_date,
                                                  date__lte=end_date)
        total_income = transactions.filter(is_expense=False).aggregate(s=Sum('amount'))['s'] or 0
        total_expense = transactions.filter(is_expense=True).aggregate(s=Sum('amount'))['s'] or 0
        remainder = min(max(budjet_obj.amount - total_expense + total_income, 0), budjet_obj.amount)

        data = request.data
        data['owner_id'] = owner_id
        data['budjet'] = budjet_obj
        data['total_income'] = total_income
        data['total_expense'] = total_expense
        data['remainder'] = remainder

        serializer = serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
