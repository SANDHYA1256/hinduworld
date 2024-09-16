from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# from .views import OrgnizationView,countries_by_Continent,CountryView,GetItemByfield_InputView,continentsView,AddOrgnization,GetOrgByStatus_Pending,GetOrgByStatus_Success,UpdateOrgStatus,Register_LoginView,Validate_LoginOTPView,GetItemByfields_InputViews,MemberDetailsViews,UpdateMemberDetails,DistrictVIew,StateViews,GetOrgbyroot_map,states_by_country,districts_By_State,GetProfileById,GetProfile
from .views import *



router=DefaultRouter()
router.register(r'organizations',OrgnizationView)
router.register(r'countries',CountryView)
router.register(r'continents',continentsView)
router.register(r'state',StateViews)  
router.register(r"district",DistrictVIew)
router.register(r'category',CategoryView)
router.register(r'subcategory',SubCategoryView)
router.register(r'events', EventsViewSet, basename='events')
router.register(r'training', TrainingView, basename='training')
router.register(r'eventcategory',EventCategoryView)
router.register(r'trainingcategory',TrainingCategoryView)



urlpatterns=[

    path('',include(router.urls)),
    path('organization_get/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
    # path('organizations_get/<str:field_name1>/<str:input_value1>/<str:field_name2>/<str:input_value2>', GetItemByfields_InputViews.as_view()),
    path('addOrgnization',AddOrgnization.as_view()),
    path('updateStatusOrgnization/<str:org_id>',UpdateOrgStatus.as_view()),
    # path('get_org_by_pending',GetOrgByStatus_Pending.as_view()),
    # path('get_org_by_success',GetOrgByStatus_Success.as_view()),
    path('get-countriesBycontinent/<str:continent>', countries_by_Continent.as_view(), name='get-items-by-field'),
    path('register_login',Register_LoginView.as_view(), name="register"),
    path('verify_login',Validate_LoginOTPView.as_view()),
    path('updateMemberDetails/<str:id>',UpdateMemberDetails.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('states_by_country/<str:country>',states_by_country.as_view()),
    path('districts_by_state/<str:state>/', districts_By_State.as_view(), name='districts_by_state'),
    path('profile_get_by_id/<str:id>/',GetProfileById.as_view()),
    path('profile_get/',GetProfile.as_view()),
    # path('events/', AddEventView.as_view(), name='add-event'),
    path('eventsupdatestatus/<uuid:event_id>/', UpdateEventStatus.as_view(), name='update-event-status'),
    path('trainingupdatestatus/<uuid:training_id>/update-status/', UpdateTrainingStatus.as_view(), name='update-training-status'),
    path('eventsmain', EventsMain.as_view(), name='events-main'),
    path('organizationsmain', OrganizationMain.as_view(), name='organizations-main'),
    path('trainingsmain', TrainingMain.as_view(), name='trainings-main'),
    # path('updatetrainer/<uuid:id>/', UpdateTrainerView.as_view(), name='update_trainer'),
    # path('getTrainer/<uuid:id>/',GetTrainerView.as_view()),
    # path('updateTrainer/<uuid:id>/',UpdateTrainer.as_view()),
    # path('eventsupcoming', UpcomingEventsView.as_view(), name='upcoming-events'),
    # path('eventspast', PastEventsView.as_view(), name='past-events'),
    path('locationByEvents/', GetEventsByLocation.as_view()),
    path('locationByOrganization/',GetOrganizationsByLocation.as_view()),
    path('locationByTraining/',GetTrainingsByLocation.as_view()),
    # path('eventsstatus', EventstatusView.as_view(), name='event-list'),
    path("home",HomeView.as_view()),








]


