from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Enfant, Parent, Staff
from rest_framework.decorators import api_view
from .serializers import EnfantSerializer, ParentSerializer, StaffSerializer
from  rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets

# Create your views here.
# 1. Without REST and no model query
def no_rest_no_model(request):
    parents = [
        {'id': 1, 'nom': 'Doe', 'prenom': 'John', 'telephone': '1234567890', 'email': 'edrfgbgr'},
        {'id': 2, 'nom': 'Smith', 'prenom': 'Jane', 'telephone': '0987654321', 'email': 'qazwsxedc'}
    ]

    return JsonResponse(parents, safe=False)
#2. mopdel data default django without rest
def no_rest_from_model(request):
    data = Enfant.objects.all()
    response={
        "enfants":list(data.values("nom","prenom","date_naissance","sexe","groupe","date_inscription","allergies","remarques_medicales")),
    }
    return JsonResponse(response)
#list  ==GET
#create ==POST
#pk query ==GET 
#update ==PUT
#delete destory ==DELETE

#3 function based views 
#3.1 GET POST
@api_view(['GET','POST'])
def FBV_list(request):
    if request.method == 'GET':
        enfants = Enfant.objects.all()
        serializer = EnfantSerializer(enfants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EnfantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#3.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):
    try:
        enfant = Enfant.objects.get(pk=pk)
    except Enfant.DoesNotExist:
        return Response({'error': 'Enfant non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        serializer = EnfantSerializer(enfant)  # هنا بدون many=True
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        serializer = EnfantSerializer(enfant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        enfant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#CBV class based views
#4.1 list and create == GET and  POST
class CBV_List(APIView):
    def get(self, request):
        enfants = Enfant.objects.all()
        serializer = EnfantSerializer(enfants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EnfantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#4.2 GET PUT DELETE
class CBV_Pk(APIView):
    def get_object(self, pk):
        try:
            return Enfant.objects.get(pk=pk)
        except Enfant.DoesNotExist:
            return None

    def get(self, request, pk):
        enfant = self.get_object(pk)
        if enfant is None:
            return Response({'error': 'Enfant non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EnfantSerializer(enfant)
        return Response(serializer.data)

    def put(self, request, pk):
        enfant = self.get_object(pk)
        if enfant is None:
            return Response({'error': 'Enfant non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EnfantSerializer(enfant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        enfant = self.get_object(pk)
        if enfant is None:
            return Response({'error': 'Enfant non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        enfant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#5 Mixins
#5.1 mixins list 
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
#5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
#6 generics
#6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer


#6.2 get put and delete   
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer

#7viewsets
class viwsets_enfant(viewsets.ModelViewSet):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer

class viwsets_parent(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom']



class viwsets_staff(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

#8 find parent
@api_view(['GET'])
def find_parent(request):
    nom = request.query_params.get('nom')
    prenom = request.query_params.get('prenom')
    parents = Parent.objects.filter(
        nom=nom,
        prenom=prenom
    ) 
    serializer = ParentSerializer(parents, many=True)
    return Response(serializer.data)
#9 create new enfant
@api_view(['POST'])
def new_enfant(request):
    # 1️⃣ récupérer parent
    parent_id = request.data.get('parent_id')
    if not parent_id:
        return Response(
            {"error": "parent_id est requis"},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        parent = Parent.objects.get(id=parent_id)
    except Parent.DoesNotExist:
        return Response(
            {"error": f"Parent avec ID {parent_id} introuvable. Créez d'abord un parent."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2️⃣ récupérer educateur (optionnel)
    educateur = None
    educateur_id = request.data.get('educateur_id')
    if educateur_id:
        try:
            educateur = Staff.objects.get(id=educateur_id)
        except Staff.DoesNotExist:
            return Response(
                {"error": "Educateur introuvable"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # 3️⃣ créer enfant
    enfant = Enfant.objects.create(
        nom=request.data.get('enfant_nom'),
        prenom=request.data.get('enfant_prenom'),
        date_naissance=request.data.get('enfant_date_naissance'),
        sexe=request.data.get('enfant_sexe'),
        groupe=request.data.get('enfant_groupe'),
        allergies=request.data.get('enfant_allergies', ''),
        remarques_medicales=request.data.get('enfant_remarques_medicales', ''),
        parent=parent,
        educateur=educateur
    )

    return Response(
        {
            "message": "Enfant créé avec succès",
            "enfant_id": enfant.id
        },
        status=status.HTTP_201_CREATED
    )



