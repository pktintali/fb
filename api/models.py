
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    premium = models.BooleanField(default=False)
    redeemedPremium = models.BooleanField(default=False,verbose_name='Redeemed')
    coins = models.IntegerField(default=50)
    shared_fact_counts = models.IntegerField(default=0,verbose_name='Shared')
    last_seen = models.DateTimeField(auto_now=True)
    streak = models.IntegerField(default=0)
    premium_start_date = models.DateField(null=True,blank=True)
    premium_end_date = models.DateField(null=True,blank=True)
    avtar = models.IntegerField(default=0, blank=True, null=True)

#! Note this import should not go on top  
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Using Custom AuthModel to Allow user login with either username or password
class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                UserModel().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class Category(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=20,default='english')
    desc= models.CharField(max_length=50, null=True)
    imgURL = models.URLField(null=True)
    isPremium = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Fact(models.Model):
    fact = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    imgURL = models.URLField(null=True)
    imgURL2 = models.URLField(null=True, blank=True)
    ref = models.URLField(null=True, blank=True)
    desc = models.TextField(blank=True, null=True)
    isAd = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        # return self.fact[:20]
        return self.fact[:150]


class DailyFact(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)


class BookMark(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fact', 'user',)


class Like(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fact', 'user',)


class Reward(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    duration = models.IntegerField()
    cost = models.IntegerField()
    imgURL = models.URLField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


#! Not in use in production
class Subscription(models.Model):
    cost = models.IntegerField()
    type = models.CharField(max_length=20)
    duration = models.IntegerField()
    description = models.CharField(max_length=50, null=True)


class UserTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_number = models.IntegerField()
    
    class Meta:
        unique_together = ('user', 'task_number',)


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category',)


class CategoryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    response = models.CharField(max_length=500,null=True,blank=True)
    # Status 0 Waiting, Status 1 Accepted, Status 2 Rejected
    status = models.IntegerField(default=0)


class ReportFact(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    reason = models.TextField()
    description = models.TextField()

    class Meta:
        unique_together = ('fact', 'email',)


class Views(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    class Meta:
        unique_together = ('fact', 'user',)
    
    def save(self, *args, **kwargs):
        self.expiry_date = timezone.now() + timezone.timedelta(days=60)
        super().save(*args, **kwargs)
        
        
class Analytics(models.Model):
    ACTIVITY_CHOICES = [
        ('TOUR_SKIPPED', 'User skipped initial app tour'),
        ('TOUR_COMPLETED', 'User completed initial app tour'),
        ('INTEREST_SELECTION_SKIPPED', 'User did not selected any category on selection in onboarding'),
        ('CATEGORY_TO_SUBSCRIPTION', 'User wen on subscription page from selecting premium category during onboarding'),
        ('DASHBOARD_VISIT', 'User visited dashboard in signup session'),
        ('COIN_PAGE_VISIT', 'User visited coin page from home coin button in signup session'),
        ('PROFILE_VISIT', 'User visited profile page from home profile button in signup session'),
        ('REWARD_PAGE_VISIT', 'User clicked redeem coin button in signup session'),
        ('SWIPE_DOWN_BACK', 'User used the swipe down option of stack cards in signup session'),
        ('AD_SWIPED', 'User successfully swiped the ad card in signup session'),
        ('REMOVE_AD_AUTH', 'Logged in User clicked remove ad on google ad card and went on subscription page in initial session'),
        ('STORE_RATING_POPUP', 'User opened the final play store rating popup'),
        ('STORE_RATING_NO_POPUP', 'User tried opening the play store rating popup but store rating not available'),
        ('STORE_RATING_WEB_POPUP', 'User opened the play store rating popup on web platform'),
        ('STORE_POPUP_FEEDBACK', 'User opened feedback while rating on store popup'),
        ('STORE_POPUP_FEEDBACK_CANCEL', 'User saw feedback and canceled on store_popup'),
        ('RATE_1S', 'User selected 1 star rating and clicked proceed'),
        ('RATE_2S', 'User selected 2 star rating and clicked proceed'),
        ('RATE_3S', 'User selected 3 star rating and clicked proceed'),
        ('RATE_4S', 'User selected 4 star rating and clicked proceed'),
        ('RATE_5S', 'User selected 5 star rating and clicked proceed'),
        ('RATING_POPUP', 'User opened the rating popup'),
        ('PROFILE_FEEDBACK_CLICK', 'User clicked feedback button from profile'),
        ('PROFILE_TOUR_CLICK', 'User clicked tour button from profile'),
        ('PROFILE_PRIVACY_CLICK', 'User clicked privacy and policy button from profile'),
        ('PROFILE_SIGNOUT', 'Real User signed out from profile'),
        ('PROFILE_CATEGORY_VISIT', 'User opened category option from profile in initial session'),
        ('PROFILE_FAVORITE_VISIT', 'User opened favorite page from profile'),
        ('PROFILE_BOOKMARK_VISIT', 'User opened bookmark page from profile'),
        ('PROFILE_ACCOUNT_VISIT', 'User opened account setting page from profile'),
        ('PROFILE_SETTING_VISIT', 'User opened app setting page from profile in initial session'),
        ('PROFILE_FAQ_VISIT', 'User opened app faq page from profile'),
        ('DASHBOARD_SEARCH', 'User clicked search icon from dashboard'),
        ('DASHBOARD_VIEW_ALL', 'User clicked view all button from dashboard'),
        ('LEARN_MORE', 'User clicked learn more in card in initial session'),
        ('CARD_CATEGORY_CLICK', 'User clicked on category name in the card'),
        ('THEME_CHANGED_DARK', 'User changed theme to dark mode'),
        ('THEME_CHANGED_LIGHT', 'User changed theme to light mode'),
        ('DATA_SAVER_ON', 'User turned on data saver mode'),
        ('DATA_SAVER_OFF', 'User turned off data saver mode'),
        ('STACKED_OFF', 'User turned off stacked layout'),
        ('STACKED_ON', 'User turned on stacked layout'),
        ('LANGUAGE_SETTING', 'User opened the language setting from profile'),
        ('AUTH_FONT_SETTING', 'User clicked font setting from app setting'),
        ('PROFILE_CHANGE_AVATAR', 'User clicked change avatar from profile page'),
        ('FONT_PADUK', 'User changed font to paduk'),
        ('FONT_KALAM', 'User changed font to kalam'),
        ('FONT_MUKTA', 'User changed font to mukta'),
        ('FONT_PATRICK_HAND', 'User changed font to patrick hand'),
        ('FONT_POPPINS', 'User changed font to  poppins'),
        ('FONT_CRIMSON_TEXT', 'User changed font to  crimson text'),
        ('FONT_NOTO', 'User changed font to noto'),
        ('CATEGORY_SELECT_NEW', 'User clicked on select new category from category settings'),
        ('CATEGORY_SELECTED_CATEGORIES', 'User clicked on selected categories from category settings'),
        ('CATEGORY_REQUEST', 'User clicked on category request from category settings'),
        ('CATEGORY_REQUEST_STATUS', 'User clicked on check status on category request page'),
        ('ACCOUNT_NAME_UPDATE', 'User clicked on name update from account setting'),
        ('ACCOUNT_AVATAR_CHANGE', 'User clicked on change avatar from account setting'),
        ('ACCOUNT_EMAIL_CLICK', 'User clicked on email option from account setting'),
        ('ACCOUNT_PASSWORD_RESET', 'User clicked on reset password option from account setting'),
        ('ACCOUNT_MANAGE_SUBSCRIPTION', 'User clicked on manage subscription option from account setting'),
        ('ACCOUNT_SIGNOUT', 'Real User clicked on sign out button from account setting'),
        ('ACCOUNT_SIGNOUT_COMPLETED', 'Real User signed out from account setting'),
        ('DASHBOARD_PREMIUM_CARD_AUTH', 'User clicked premium card on dashboard'),
        ('DASHBOARD_COIN_WIDGET_AUTH', 'User clicked coin widget on dashboard'),
        ('PLANS_MANAGE_SUBSCRIPTION', 'User clicked manage subscriptions from subscription page'),
        ('RESTORED_PURCHASE', 'User clicked restore purchase from subscription page'),
        ('BUY_CLICKED', 'User clicked a premium plan to buy from subscription page'),
        ('APP_DOWNLOAD_WIDGET', 'User clicked app download widget on web'),
        ('SIGNUP_ERROR', 'User got input related error while signing up'),
        ('UNEXPECTED_SIGNUP_ERROR', 'User got unexpected error while signing up'),
        ('LOGIN_ERROR', 'User got input related error while log in'),
        ('UNEXPECTED_LOGIN_ERROR', 'User got unexpected error while log in'),
        ('PURCHASE_CONFIGURE_ERROR', 'User got error while configuring purchase api sdk'),      
        ('TRIED_SWIPING_ADCARD', 'User tried swiping ad card in initial session before timer'),      
        ('TRIED_SWIPING_BACK_ADCARD', 'User tried swiping back ad card in initial session before timer in'),
        
        
        ('DELETE_ACCOUNT_DATA', 'Anonymous user clicked delete account and data on account setting'),
        ('DELETE_ACCOUNT_DATA_WARNING_IGNORE', 'Anonymous user ignored delete account and data warning and logged out on account setting'),
        ('DELETE_ACCOUNT_DATA_WARNING_CONSIDERED', 'Anonymous user considered delete account and data warning on account setting'),
        ('SET_EMAIL_PASS_CLICK', 'Anonymous User clicked on set email and password to backup data from account setting'),
        ('ACCOUNT_DATA_LOST_WARNING', 'Anonymous User clicked on account data lost warning tile from account setting'),
        ('CONVERT_ERROR', 'Anonymous User got error while being converted to a real user'),
        ('CONVERT_SUCCESS', 'Anonymous User successfully converted to a real user'),
        ('CONVERT_EMAIL_EXIST_ERROR', 'Anonymous User got email already exist error while converted to a real user'),
        ('ANONYMOUS_SETUP_NO_NAME', 'User proceeded without entering name in sign up process'),
        ('ANONYMOUS_SETUP_WITH_NAME', 'User proceeded by entering name in sign up process'),
        ('ANONYMOUS_SETUP_NAME_ERROR', 'User got error related to name in anonymous setup, auth complete without name'),
        ('ANONYMOUS_SETUP_ERROR', 'User got error while anonymously proceeding'),
        ('ANONYMOUS_SETUP_SAVE_ERROR', 'User got error while saving user data'),
        ('500_PLUS_COINS', 'WAV User Now Have more than 500 coins in profile'),
        ('20_PLUS_DAYS_STREAK', 'WAV User Reached 20 Days or more of streak'),
        ('TAKEN_NOTIFICATION_ACTION', 'User clicked ok button on notification'),
        
        
        ('SKIP_WARNING_OK', '[STOPPED] - User ignored sign up skip warning - [STOPPED]'),
        ('SKIP_WARNING_CANCEL', '[STOPPED] - User considered sign up skip warning'),
        ('SIGNUP_CLICKED', '[STOPPED] - User clicked signup button from home auth'),
        ('LOGIN_CLICKED', '[STOPPED] - User clicked login button from home auth'),
        ('HOME_AUTH_SKIP', '[STOPPED] - User clicked skip from home auth page'),
        ('SIGNUP_PAGE_SKIP', '[STOPPED] - User clicked skip from signup page'),
        ('LOGIN_PAGE_SKIP', '[STOPPED] - User clicked skip from login page'),
        ('NOAUTH_SHARE_CLICK', '[STOPPED] - Non logged in user clicked share button from fact card'),
        ('NOAUTH_SPEAK_CLICK', '[STOPPED] - Non logged in user clicked speak button from fact card and went on home auth page'),
        ('REMOVE_AD_NOAUTH - [STOPPED]', 'Non Logged in User clicked remove ad on google ad card and went on home auth page'),
        ('NOAUTH_LIKE_CLICK', '[STOPPED] - Non logged in user clicked like button from fact card and went on home auth page'),
        ('NOAUTH_BOOKMARK_CLICK', '[STOPPED] - Non logged in user clicked bookmark button from fact card and went on home auth page'),
        ('NOAUTH_FONT_SETTING', '[STOPPED] - Non loggedin user clicked font setting and went on home auth'),
        ('DASHBOARD_PREMIUM_CARD_NOAUTH', '[STOPPED] - No logged in User clicked premium card on dashboard and went on home auth'),
        ('DASHBOARD_COIN_WIDGET_NOAUTH', '[STOPPED] - Non logged in User clicked coin widget on dashboard and went on home auth'),
        ('FLIP_CARD', '[STOPPED] - User flipped card in initial session excluding app tour'),
        ('AUTH_SPEAK_CLICK', '[STOPPED] - User clicked speak button from fact card and went on subscription page'),
        ('PROFILE_LOGIN_CLICK', '[Unreachable] - User clicked login page from profile'),
        ('IMAGE_CLICK', '[STOPPED] - User clicked on image in the card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    activity = models.CharField(choices=ACTIVITY_CHOICES,max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True) 
    
    
class AppNotification(models.Model):
        
    PAGE_CHOICES = [
    ('APP_SETTINGS', 'APP_SETTINGS'),
    ('ACCOUNT_SETTINGS', 'ACCOUNT_SETTINGS'),
    ('FONT_SETTINGS', 'FONT_SETTINGS'),
    ('LANGUAGE_SETTINGS', 'LANGUAGE_SETTINGS'),
    ('AVATAR_SETTINGS', 'AVATAR_SETTINGS'),
    ('ACCOUNT_BACKUP', 'ACCOUNT_BACKUP'),
    ('RATING_POPUP', 'RATING_POPUP'),
    ('CATEGORY_REQUEST', 'CATEGORY_REQUEST'),
    ('CATEGORY_REQUEST_STATUS', 'CATEGORY_REQUEST_STATUS'),
    ('CATEGORY_ADD', 'CATEGORY_ADD'),
    ('COIN_PAGE', 'COIN_PAGE'),
    ('SEARCH_PAGE', 'SEARCH_PAGE'),
    ('DASHBOARD_PAGE', 'DASHBOARD_PAGE'),
    ('PREMIUM_PAGE', 'PREMIUM_PAGE'),
    ('CATEGORY_VIEW_ALL', 'CATEGORY_VIEW_ALL'),
    ]
    
    ALERT_TYPES = [
        ('INFO','INFO'),
        ('INFO_REVERSED','INFO_REVERSED'),
        ('WARNING','WARNING'),
        ('ERROR','ERROR'),
        ('SUCCESS','SUCCESS'),
        ('QUESTION','QUESTION'),
        ('NO_HEADER','NO_HEADER')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    type = models.CharField(choices=ALERT_TYPES,max_length=50)
    closeButton = models.BooleanField(default=False)
    btnOkText = models.CharField(max_length=25,null=True,blank=True)
    btnCancelText = models.CharField(max_length=25,null=True,blank=True)
    isBtnOkLink = models.BooleanField(default=False)
    btnOkLink = models.URLField(blank=True,null=True)
    targetPage = models.CharField(choices=PAGE_CHOICES,max_length=50,null=True,blank=True)