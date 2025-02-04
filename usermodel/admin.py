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
from django.contrib.auth.admin import UserAdmin
from usermodel.models import User, Profile
from django.contrib.sessions.models import Session


class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_staff')
	search_fields = ('email', 'username',)
	readonly_fields = ('date_joined', 'last_login', 'pk',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(User, AccountAdmin)


admin.site.register(Profile)



admin.site.register(Session)