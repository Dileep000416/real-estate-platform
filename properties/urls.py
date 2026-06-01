from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),
    path('add-property/', views.add_property, name='add_property'),
    path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),
path(
    'edit-property/<int:id>/',
    views.edit_property,
    name='edit_property'
),

path(
    'delete-property/<int:id>/',
    views.delete_property,
    name='delete_property'
),
path(
    'logout/',
    views.logout_view,
    name='logout'
),
path(
    'toggle-favorite/<int:id>/',
    views.toggle_favorite,
    name='toggle_favorite'
),
path(
    'review/<int:id>/',
    views.add_review,
    name='add_review'
),

path(
    'favorites/',
    views.favorites_page,
    name='favorites'
),

path(
    'inquiry/<int:id>/',
    views.send_inquiry,
    name='send_inquiry'
),

path(
    'compare/<int:property_id>/',
    views.add_to_compare,
    name='add_to_compare'
),

path(
    'compare-properties/',
    views.compare_properties,
    name='compare_properties'
),
path(
    'schedule-visit/<int:id>/',
    views.schedule_visit,
    name='schedule_visit'
),
path(
    'chat/<int:property_id>/<int:user_id>/',
    views.chat_view,
    name='chat'
),
path(
    'inbox/',
    views.inbox,
    name='inbox'
),
path(
    'notifications/',
    views.notifications_page,
    name='notifications'
),
path(
    'agent/<int:id>/',
    views.agent_profile,
    name='agent_profile'
),
path(
    'owner-inquiries/',
    views.owner_inquiries,
    name='owner_inquiries'
),
path(
    'owner-visits/',
    views.owner_visits,
    name='owner_visits'
),

path(
    'owner-favorites/',
    views.owner_favorites,
    name='owner_favorites'
),

path(
    'buyer-favorites/',
    views.buyer_favorites,
    name='buyer_favorites'
),

path(
    'buyer-recent/',
    views.buyer_recent,
    name='buyer_recent'
),

path(
    'buyer-inquiries/',
    views.buyer_inquiries,
    name='buyer_inquiries'
),
path(
    'edit-profile/',
    views.edit_profile,
    name='edit_profile'
),
path(
    'users-list/',
    views.users_list,
    name='users_list'
),
path(
    'reset-render-admin/',
    views.reset_render_admin,
    name='reset_render_admin'
),

]