from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from api.models import Company
from api.serializers import CompanySerializer


class CompanyList(APIView):
    """
    List all companies, or create a new company.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanyDetail(APIView):
    """
    Retrieve, update or delete a company instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, company_uuid):
        return Company.objects.get(uuid=company_uuid)

    def get(self, request, company_uuid, format=None):
        company = self.get_object(company_uuid)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, company_uuid, format=None):
        company = self.get_object(company_uuid)
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, company_uuid, format=None):
        company = self.get_object(company_uuid)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
