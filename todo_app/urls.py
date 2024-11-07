from django.urls import path
from . import views

urlpatterns = [
    path('' , views.indexPage , name='home'),
    path('login/' , views.loginPage , name='login'),
    path('register/' , views.registerPage , name='register'),
    path('delete/<str:todo_id>/' , views.deleteView , name='delete'),
    path('updatestatus/<str:todo_id>/' , views.updateStatus , name='update'),
    path("logout/", views.logoutView , name="logout"),
    path("forget_password/" ,  views.ForgetPassword , name='forgetpassword'   ),
    path("password_reset_sent/<str:reset_id>/"  , views.passwordResetSent , name='passwordresetsent' ),
    path("reset_password/<str:reset_id>/" , views.resetPassword , name='resetpassword'),
    path('test/' , views.test , name='test'),
    path('edit_task/<str:todo_id>' , views.edittask , name='edittask')

]

