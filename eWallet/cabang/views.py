from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Customer
from .serializer import CustomerSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from . import services
import json

class CustomerViewSet(viewsets.ViewSet):
    queryset = Customer.objects.all()

    @action(detail=False, methods=['get'])
    def index(self, request, pk=None):
        users = Customer.objects.all()
        template = loader.get_template('cabang/index.html')
        context = {
            'users': users,
        }
        return HttpResponse(template.render(context, request))

    @action(detail=False, methods=['post'])
    def register(self, request, pk=None):
        quorum = services.check_active_cabang()
        if quorum == -2:
            return Response({'registerReturn': quorum})

        print(request.data)
        customerSerializer = CustomerSerializer(data=request.data)

        try:
            customerSerializer.is_valid(raise_exception=True)
        except:
            return Response({'registerReturn': -99})

        try:
            customerSerializer.save()
            return Response({'registerReturn': 1})
        except:
            return Response({'registerReturn': -4})  

        return Response({'registerReturn': -99})


    @action(detail=False, methods=['post'])
    def getSaldo(self, request, pk=None):
        saldo = self.status_saldo(request.data.get('user_id'))
        return Response({'saldo': saldo})

    def status_saldo(self, user_id):
        customer = Customer.objects.filter(user_id=user_id).first()

        if not customer:
            return -1

        quorum = services.check_active_cabang()
        if quorum == -2:
            return quorum

        return customer.saldo


    @action(detail=False, methods=['post'])
    def ping(self, request, pk=None):
        try:
            return Response({'pingReturn': 1})
        except:
            return Response({'pingReturn': -99})


    @action(detail=False, methods=['post'])
    def transfer(self, request, pk=None):
        status_tranfer = self.status_tranfer(request.data.get('user_id'), request.data.get('nilai'))
        return Response({'transferReturn': status_tranfer})

    def status_tranfer(self, user_id, nilai):

        customer = Customer.objects.filter(user_id=user_id).first()

        if not customer:
            return -1

        quorum = services.check_active_cabang()
        if quorum == -2:
            return quorum

        saldo = int(nilai)
        if saldo < 0 or saldo > 1000000000:
            return -5

        try:
            customer.saldo = customer.saldo + saldo
            customer.save()
        except:
            return -4

        return 1

    @action(detail=False, methods=['post'])
    def transferTo(self, request, pk=None):
        message = ''
        user_id = request.data.get('user_id')
        ip = request.data.get('ip')
        saldo = request.data.get('saldo')
        users = Customer.objects.all()
        customer = Customer.objects.filter(user_id=user_id).first()
        
        if customer:
            current_saldo = customer.saldo - int(saldo)
            if current_saldo < 0:
                message = 'Saldo overlimit'
            else:
                status = services.transfer_saldo(user_id, ip, saldo)
                if status == 1:
                    message = 'transfer success'
                    customer.saldo = current_saldo
                    customer.save()
                elif status == -1:
                    message = 'user_id is not registered in ' + ip
                else:
                    message = 'Something wrong on the other side ...'
        else:
            message = 'Invalid user_id'

        template = loader.get_template('cabang/index.html')
        context = {
            'users': users,
            'message': message
        }
        print(message)
        return HttpResponse(template.render(context, request))
    
    @action(detail=False, methods=['post'])
    def getTotalSaldo(self, request, pk=None):
        status_total_saldo = self.status_total_saldo(request.data.get('user_id'))
        return  Response({'saldo' : status_total_saldo})

    def status_total_saldo(self, user_id):
        
        customer = Customer.objects.filter(user_id=user_id).first()

        if not customer:
            return -1

        if customer.is_domisili:
            quorum = services.check_active_cabang()
            if quorum != 2:
                return -2
                
            total_saldo = int(customer.saldo) + services.request_saldo_to_all_cabang(user_id)
            return total_saldo
        else:
            return services.request_get_total_saldo(user_id)