# Copyright [2021] [FORTH-ICS]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.base import TemplateView

from landingpageapp.views import (
     landing_page_form_view,
)

from mymainapp.views import (
    home_screen_view,
    frontpage_view,
    profile_view,
    CandleList_view,
    ReviewList_view,
    candle_detail_view,
    candle_list_view,
    about_view,
    brand_create_view,
    candle_create_view,
    review_candle_create_view,
    report_review_create_view,
)

from usermodel.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,

)

urlpatterns = [
    path('sadmin/', admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('select2/', include('django_select2.urls')),
    # path('home2/', home_screen_view, name="home"),
    path('', landing_page_form_view.as_view(), name="landing-page"),
    path('<int:referral_option>/', landing_page_form_view.as_view(), name="landing-page-with-referral"),
    path('home/', frontpage_view, name="frontpage"),
    path('profile/<str:usn>', profile_view, name="profile"),
    path('candles/', candle_list_view, name="candles"),
    path('reviews/', ReviewList_view.as_view(), name="reviews"),
    path('candles/<int:pk>/', candle_detail_view, name="candle-detail"),
    path('about/' , about_view, name="about"),
    path('brands/add/', brand_create_view.as_view(), name="brand-add-form"),
    path('candles/add/', candle_create_view.as_view(), name="candle-add-form"),
    path('candles/review/add/<int:candle_id>', review_candle_create_view.as_view(), name="review-add-form"),
    path('reports/add/<int:report_type_id>/<int:review_id>', report_review_create_view.as_view(), name="report-add-form"),
    # path('candles/listitems/add/<int:candle_id>')
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account_detail"),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)