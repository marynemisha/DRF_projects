from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Repository.models import *
from Repository.serializers import *
from Repository.gemini_service import evaluate_answer
import json
# Create your views here.
class QuestionsListViewCreate(APIView):
    def get(self,request):
        qs=QuestionsDb.objects.all()
        serializer_instance=QuestionsDbSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    #post method for adding questions
    def post(self,request):
        form_data=request.data  #get the form data from the request
        serializer_instance=QuestionsDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            original_data=serializer_instance.validated_data  #GET THE VALIDATED DATA FROM THE 
            #create a new question instance using the form data
            QuestionsDb.objects.create(**original_data)     #UNPACK THE VALIDATED DATA AND CREATE
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class QuestionsRetrieveUpdateDelete(APIView):
    def get(self,request,pk):
        qs= QuestionsDb.objects.get(id=pk)
        serializer_instance=QuestionsDbSerializer(qs)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        form_data=request.data
        serializer_instance=QuestionsDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            actual_data=serializer_instance.validated_data
            QuestionsDb.objects.filter(id=pk).update(**actual_data)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
    def delete(self,request,pk):
        QuestionsDb.objects.filter(id=pk).delete()
        return Response(
            {"message":"Question Deleted successfully..!"}
        )

class SubmissionListCreateView(APIView):
    def get(self,request):
        qs=SubmissionsDb.objects.all()
        serializer_instance=SubmissionSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=SubmissionSerializer(data=form_data)
        if serializer_instance.is_valid(): 
            original=serializer_instance.validated_data

            #step1- GET QUESTION FROM DATABASE(QuestionsDb)
            question=QuestionsDb.objects.get(id=original['question_id'])

            #step2-PREPARE QUESTION DETAILS
            question_details=f"""
            Title:{question.title}
            Language:{question.language}
            Difficulty:{question.difficulty_level}
            Topic:{question.topic}
            Description={question.notes}
            Sample Input:{question.sample_input}
            Sample Output:{question.sample_output}
            """

            #step3-GET STUDENT'S ANSWER
            student_answer=original["answer"]

            #step4-GET A STRUCTURED FEEDBACK FROM GEMINI
            try:
                feedback=evaluate_answer(question_details,student_answer)
            except Exception as e:
                return Response({
                    "Message":"AI evaluation failed..!",
                    "Details":str(e)
                })

            #step5-CONVERT DICTIONARY INTO JSON STRING
            feedback_json=json.dumps(feedback)

            #step6-SAVE SUBMISSION IN DATABASE
            submission=SubmissionsDb.objects.create(**original,remarks=feedback_json)

            #step7-RETURN THE STRUCTURED RESPONSE
            return Response({
                "Message":"Submitted successfully...!",
                "Answer":submission.answer,
                "AI_Feedback":feedback
            })
        else:
            return Response(serializer_instance.errors)

class submissionRetrieveUpdateDelete(APIView):
    def get(self,request,pk):
        # qs=SubmissionsDb.objects.get(id=pk)
        qs=get_object_or_404(SubmissionsDb,id=pk) #Retrieves an object by primary key; returns a 404 error if not found.
        serializer_instance=SubmissionSerializer(qs)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        form_data=request.data
        serializer_instance=SubmissionSerializer(data=form_data)
        if serializer_instance.is_valid():
            actual=serializer_instance.validated_data
            SubmissionsDb.objects.filter(id=pk).update(**actual)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
class EvaluateSubmissionView(APIView):
    def put(self,request,pk):
        form_data=request.data
        SubmissionsDb.objects.filter(id=pk).update(**form_data)
        return Response(data={
            "Message":"Updated...!"
        }); 