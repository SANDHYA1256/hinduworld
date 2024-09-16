# from ..serializers import UserSerializer,LoginSerializer,VerifySerializer,ResetSerializer,ResetSerializer,ResendOtpSerializer,RegisterSerializerl,VerifyOtpSerializer
from ..serializers import Register_LoginSerializer,Verify_LoginSerializer,MemberSerializer,MemberPicSerializer
from rest_framework import viewsets,generics
from ..models import Register
from rest_framework .views import APIView,status
from rest_framework .response import Response
from ..enums.user_status_enum import UserStatus
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import validate_email,send_email,send_sms,generate_otp,Resend_sms,send_welcome_email,image_path_to_binary,save_video_to_folder,video_path_to_binary
from django.contrib.auth import authenticate
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_folder
from datetime import datetime
from rest_framework.permissions import IsAuthenticated


     
class Register_LoginView(generics.GenericAPIView):
    serializer_class = Register_LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        
        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        message = ""
        
        try:
            user = Register.objects.using('gramadevata').get(username=username)
            # Username already exists, update OTP
            user.verification_otp = otp
            user.verification_otp_created_time = timezone.now()
            user.save(using='gramadevata')
            message = " OTP sent successfully"
        except Register.DoesNotExist:
            # Username does not exist, create new user and set OTP
            user = Register.objects.using('gramadevata').create(username=username, verification_otp=otp, verification_otp_created_time=timezone.now())
            user.save(using='gramadevata')
            message = "OTP sent successfully"

        # Determine if username is an email or phone number
        if validate_email(username):
            send_email(username, otp)
        else:
            send_sms(username, otp)

        return Response({"otp": message}, status=status.HTTP_200_OK)





class Validate_LoginOTPView(generics.GenericAPIView):
    serializer_class = Verify_LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        verification_otp = request.data.get('verification_otp')
        
        try:
            user = Register.objects.using('gramadevata').get(username=username)
        except Register.DoesNotExist:
            return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.verification_otp != verification_otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update user status to ACTIVE
        user.status = 'ACTIVE'
        user.save(using='gramadevata')

        # Send a welcome email if the username is an email
        if validate_email(username):
            send_welcome_email(username)
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'username': user.get_username(),
            'user_id': user.id
        }, status=status.HTTP_200_OK)






class MemberDetailsViews(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = MemberPicSerializer
    permission_classes = [IsAuthenticated]


class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Register.objects.all()
        response_data = []
        for item in queryset:
            item_data = MemberSerializer(item).data

            # Process profile_pic
            profile_pic_path = item.profile_pic
            if profile_pic_path:
                encoded_string = image_path_to_binary(profile_pic_path)
                item_data['profile_pic'] = encoded_string.decode('utf-8') if encoded_string else None
            else:
                item_data['profile_pic'] = None

            # Process certificate
            certificate_path = item.certificate
            if certificate_path:
                encoded_string = image_path_to_binary(certificate_path)
                item_data['certificate'] = encoded_string.decode('utf-8') if encoded_string else None
            else:
                item_data['certificate'] = None

            response_data.append(item_data)

        return Response(response_data, status=status.HTTP_200_OK)






class GetProfileById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        item = get_object_or_404(Register, id=id)
        item_data = MemberSerializer(item).data

        # Process profile_pic
        profile_pic_path = item.profile_pic
        if profile_pic_path:
            encoded_string = image_path_to_binary(profile_pic_path)
            item_data['profile_pic'] = encoded_string if encoded_string else None
        else:
            item_data['profile_pic'] = None

        # Process certificate
        certificate_path = item.certificate
        if certificate_path:
            encoded_string = image_path_to_binary(certificate_path)
            item_data['certificate'] = encoded_string if encoded_string else None
        else:
            item_data['certificate'] = None

        return Response(item_data, status=status.HTTP_200_OK)








class UpdateMemberDetails(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def put(self, request, id):
        instance = get_object_or_404(Register, id=id)
        profile_pic = request.data.get('profile_pic')
        certificate = request.data.get('certificate')

        mutable_data = request.data.copy()
        serializer = self.get_serializer(instance, data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_member'] = True
        serializer.save()

        # Profile Pic handling
        if profile_pic and profile_pic != "null":
            saved_location = save_image_to_folder(profile_pic, serializer.instance.id, serializer.instance.full_name, 'profile_pic')
            if saved_location:
                serializer.instance.profile_pic = saved_location
        else:
            serializer.instance.profile_pic = None

        # Certificate handling
        if certificate and certificate != "null":
            saved_location = save_image_to_folder(certificate, serializer.instance.id, serializer.instance.full_name, 'certificate')
            if saved_location:
                serializer.instance.certificate = saved_location
        else:
            serializer.instance.certificate = None

        serializer.instance.save()

        # Update response data
        response_data = MemberSerializer(serializer.instance).data
        if not profile_pic or profile_pic == "null":
            response_data['profile_pic'] = None
        if not certificate or certificate == "null":
            response_data['certificate'] = None
        
        return Response(response_data, status=status.HTTP_200_OK)
