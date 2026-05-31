from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .models import Property,  Inquiry, Review
from .forms import SignupForm, PropertyForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Profile
from .models import PropertyVisit
from django.core.mail import send_mail
from .models import ChatMessage
from .models import Notification
from .models import RecentlyViewed
from .models import PropertyImage
from .forms import ProfileForm
from django.http import HttpResponse

def home(request):

    properties = Property.objects.all()

    # SEARCH

    query = request.GET.get('query')

    if query:

        properties = properties.filter(

            Q(title__icontains=query) |

            Q(location__icontains=query) |

            Q(property_type__icontains=query)

        )

    # FILTERS

    property_type = request.GET.get(
        'property_type'
    )

    status = request.GET.get(
        'status'
    )

    sort = request.GET.get(
        'sort'
    )

    if property_type:

        properties = properties.filter(
            property_type=property_type
        )

    if status:

        properties = properties.filter(
            status=status
        )

    # SORTING

    if sort == "low":

        properties = properties.order_by(
            'price'
        )

    elif sort == "high":

        properties = properties.order_by(
            '-price'
        )

    elif sort == "latest":

        properties = properties.order_by(
            '-id'
        )

    # PAGINATION

    paginator = Paginator(
        properties,
        4
    )
def create_render_admin(request):

    if User.objects.filter(username="superadmin").exists():
        return HttpResponse("Superadmin already exists")

    User.objects.create_superuser(
        username="superadmin",
        email="yourgmail@gmail.com",
        password="YourStrongPassword123"
    )

    return HttpResponse("Superadmin created")
    page_number = request.GET.get(
        'page'
    )

    properties = paginator.get_page(
        page_number
    )

    return render(

        request,

        'home.html',

        {
            'properties': properties
        }

    )
def signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            login(request, user)
            return redirect('home')

    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def property_detail(request, id):

    property = Property.objects.get(id=id)

    if request.user.is_authenticated:

        RecentlyViewed.objects.update_or_create(
            user=request.user,
            property=property
        )

        recent_properties = RecentlyViewed.objects.filter(
            user=request.user
        ).exclude(
            property=property
        )[:4]

    else:

        recent_properties = []

    gallery_images = PropertyImage.objects.filter(
        property=property
    )

    reviews = property.review_set.all()

    total_reviews = reviews.count()

    average_rating = 0

    if total_reviews > 0:

        total = 0

        for review in reviews:

            total += review.rating

        average_rating = round(
            total / total_reviews,
            1
        )

    related_properties = Property.objects.filter(
        property_type=property.property_type,
        location=property.location
    ).exclude(
        id=property.id
    )[:4]

    return render(
        request,
        'property_detail.html',
        {
            'property': property,
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'related_properties': related_properties,
            'recent_properties': recent_properties,
            'gallery_images': gallery_images
        }
    )
@login_required
def add_property(request):

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            property = form.save(commit=False)

            property.agent = request.user

            property.save()

            return redirect('dashboard')

    else:

        form = PropertyForm()

    return render(
        request,
        'add_property.html',
        {'form':form}
    )
@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
    user=request.user
)

    # =========================
    # OWNER DASHBOARD
    # =========================

    if profile.role == 'owner':

        properties = Property.objects.filter(
            agent=request.user
        ).order_by('-id')

        inquiries = Inquiry.objects.filter(
            property__agent=request.user
        ).order_by('-created_at')

        visits = PropertyVisit.objects.filter(
            property__agent=request.user
        )

        total_properties = properties.count()

        total_inquiries = inquiries.count()

        total_visits = visits.count()

        total_favorites = 0

        for property in properties:

            total_favorites += property.favorites.count()

        context = {

            'properties': properties,

            'inquiries': inquiries,

            'total_properties': total_properties,

            'total_inquiries': total_inquiries,

            'total_visits': total_visits,

            'total_favorites': total_favorites,
        }

        return render(
            request,
            'dashboard.html',
            context
        )

    # =========================
    # BUYER DASHBOARD
    # =========================

    else:

        favorite_properties = request.user.favorite_properties.all()

        recent_properties = RecentlyViewed.objects.filter(
            user=request.user
        )[:4]

        inquiries = Inquiry.objects.filter(
            user=request.user
        ).order_by('-created_at')

        total_favorites = favorite_properties.count()

        total_recent = recent_properties.count()

        total_inquiries = inquiries.count()

        context = {

            'favorite_properties': favorite_properties,

            'recent_properties': recent_properties,

            'inquiries': inquiries,

            'total_favorites': total_favorites,

            'total_recent': total_recent,

            'total_inquiries': total_inquiries,
        }

        return render(
            request,
            'buyer_dashboard.html',
            context
        )


@login_required
def delete_property(request,id):

    property=Property.objects.get(
        id=id,
        agent=request.user
    )

    property.delete()

    return redirect(
        'dashboard'
    )


@login_required
def edit_property(request,id):

    property=Property.objects.get(
        id=id,
        agent=request.user
    )

    if request.method=="POST":

        form=PropertyForm(
            request.POST,
            request.FILES,
            instance=property
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard'
            )

    else:

        form=PropertyForm(
            instance=property
        )

    return render(
        request,
        'add_property.html',
        {'form':form}
    )
def logout_view(request):

    logout(request)

    return redirect('home')

@login_required
def add_review(request, id):

    property = Property.objects.get(id=id)

    already_reviewed = Review.objects.filter(
        property=property,
        user=request.user
    ).exists()

    if already_reviewed:

        return redirect(
            'property_detail',
            id=property.id
        )

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.property = property

            review.user = request.user

            review.save()

    return redirect(
        'property_detail',
        id=property.id
    )

@login_required
def toggle_favorite(request, id):

    if request.method == "POST":

        property = Property.objects.get(id=id)

        saved = False

        if request.user in property.favorites.all():

            property.favorites.remove(request.user)

            saved = False

        else:

            property.favorites.add(request.user)

            saved = True

        return JsonResponse({

            'saved': saved

        })
@login_required
def favorites_page(request):

    properties = request.user.favorite_properties.all()

    return render(
        request,
        'favorites.html',
        {
            'properties': properties
        }
    )



@login_required
def send_inquiry(request, id):

    property = Property.objects.get(id=id)

    if request.method == "POST":

        message = request.POST.get(
            'message'
        )

        Inquiry.objects.create(
            property=property,
            user=request.user,
            message=message
        )

        Notification.objects.create(
            user=property.agent,
            message=f"{request.user.username} sent inquiry for {property.title}"
        )

        send_mail(
            'New Property Inquiry',

            f'''
Property:
{property.title}

From:
{request.user.username}

Message:
{message}
            ''',

            'janupaladileep419@gmail.com',

            [property.agent.email],

            fail_silently=False,
        )

    return redirect('dashboard')

def add_to_compare(request, property_id):

    compare_list = request.session.get(
        'compare_list',
        []
    )

    if property_id not in compare_list:

        compare_list.append(property_id)

    request.session['compare_list'] = compare_list

    return redirect(
        'compare_properties'
    )


def compare_properties(request):

    compare_list = request.session.get(
        'compare_list',
        []
    )

    properties = Property.objects.filter(
        id__in=compare_list
    )

    return render(
        request,
        'compare.html',
        {
            'properties': properties
        }
    )

@login_required
def schedule_visit(request, id):

    property = Property.objects.get(id=id)

    if request.method == "POST":

        visit_date = request.POST.get(
            'visit_date'
        )

        visit_time = request.POST.get(
            'visit_time'
        )

        PropertyVisit.objects.create(
            property=property,
            visitor=request.user,
            visit_date=visit_date,
            visit_time=visit_time
        )

        return redirect(
            'property_detail',
            id=id
        )

    return redirect(
        'property_detail',
        id=id
    )


@login_required
def chat_view(request, property_id, user_id):

    property = Property.objects.get(id=property_id)

    receiver = User.objects.get(id=user_id)

    messages = ChatMessage.objects.filter(
        property=property,
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    if request.method == "POST":

        message = request.POST.get('message')

        ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            property=property,
            message=message
        )

        Notification.objects.create(
            user=receiver,
            message=f"New message from {request.user.username}"
        )

        return redirect(
            'chat',
            property_id=property.id,
            user_id=receiver.id
        )

    context = {
        'property': property,
        'receiver': receiver,
        'messages': messages,
    }

    return render(
        request,
        'chat.html',
        context
    )
@login_required
def inbox(request):

    sent_messages = ChatMessage.objects.filter(
        sender=request.user
    )

    received_messages = ChatMessage.objects.filter(
        receiver=request.user
    )

    chats = sent_messages.union(
        received_messages
    ).order_by('-timestamp')

    context = {
        'chats': chats
    }

    return render(
        request,
        'inbox.html',
        context
    )


@login_required
def notifications_page(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'notifications.html',
        {
            'notifications': notifications
        }
    )
def agent_profile(request, id):

    agent = User.objects.get(id=id)

    properties = Property.objects.filter(
        agent=agent
    )

    context = {
        'agent': agent,
        'properties': properties
    }

    return render(
        request,
        'agent_profile.html',
        context
    )

@login_required
def owner_inquiries(request):

    inquiries = Inquiry.objects.filter(
        property__agent=request.user
    ).order_by('-created_at')

    context = {

        'inquiries': inquiries

    }

    return render(
        request,
        'owner_inquiries.html',
        context
    )

@login_required
def owner_visits(request):

    visits = PropertyVisit.objects.filter(
        property__agent=request.user
    ).order_by('-visit_date')

    context = {

        'visits': visits

    }

    return render(
        request,
        'owner_visits.html',
        context
    )


@login_required
def owner_favorites(request):

    properties = Property.objects.filter(
        agent=request.user
    )

    context = {

        'properties': properties

    }

    return render(
        request,
        'owner_favorites.html',
        context
    )

@login_required
def buyer_favorites(request):

    properties = request.user.favorite_properties.all()

    context = {
        'properties': properties
    }

    return render(
        request,
        'buyer_favorites.html',
        context
    )


@login_required
def buyer_recent(request):

    recent_properties = RecentlyViewed.objects.filter(
        user=request.user
    ).order_by('-viewed_at')

    context = {
        'recent_properties': recent_properties
    }

    return render(
        request,
        'buyer_recent.html',
        context
    )


@login_required
def buyer_inquiries(request):

    inquiries = Inquiry.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'inquiries': inquiries
    }

    return render(
        request,
        'buyer_inquiries.html',
        context
    )

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'edit_profile.html',
        {
            'form': form
        }
    )

        
@staff_member_required
def users_list(request):

    users = User.objects.all().order_by('-date_joined')

    return render(
        request,
        'users_list.html',
        {
            'users': users
        }
    )


def create_render_admin(request):

    if User.objects.filter(username="superadmin").exists():
        return HttpResponse("Superadmin already exists")

    User.objects.create_superuser(
        username="superadmin",
        email="yourgmail@gmail.com",
        password="YourStrongPassword123"
    )

    return HttpResponse("Superadmin created")