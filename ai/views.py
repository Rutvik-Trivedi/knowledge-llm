from django.db import models
from rest_framework import status, views
from rest_framework.response import Response

from ai.enums import Sentiment
from ai.extraction import extract_structured_info
from ai.models import StructuredInfo
from ai.serializers import StructuredInfoSerializer


class StructuredDataExtractionView(views.APIView):
    serializer_class = StructuredInfoSerializer

    def post(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        if not text or not text.strip():
            return Response(
                {"error": "Text field must not be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        api_key = request.headers.get("X-Api-Key", "").strip()
        if not api_key:
            return Response(
                {"error": "X-Api-Key header is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = extract_structured_info(text, api_key=api_key)
        if isinstance(response, str):
            return Response(
                {"error": response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        response_serializer = StructuredInfoSerializer(response)
        response = response_serializer.data
        response["sentiment"] = Sentiment.__labels__.get(response["sentiment"])
        return Response(response, status=status.HTTP_200_OK)


class StructuredDataSearchView(views.APIView):

    serializer_class = StructuredInfoSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("topic", "").strip()
        query = [q.strip() for q in query.split(",") if q.strip()]
        if not query:
            return Response(
                {"error": "Query parameter 'topic' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        results = []
        for single_query in query:
            # Fetch all distinct StructuredInfo entries that have the topic in their topics list and keywords list
            structured_infos = StructuredInfo.objects.filter(
                models.Q(topics__icontains=single_query)
                | models.Q(keywords__icontains=single_query)
            ).distinct()
            results.extend(list(structured_infos))
        serializer = StructuredInfoSerializer(structured_infos, many=True)
        response = serializer.data
        for item in response:
            item["sentiment"] = Sentiment.__labels__.get(item["sentiment"])
        return Response(response, status=status.HTTP_200_OK)
