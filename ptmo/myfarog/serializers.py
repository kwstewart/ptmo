from rest_framework import serializers, response

class CharacterSerializer(serializers.ModelSerializer):

    signup_date         = serializers.DateTimeField(format='%Y-%m-%d @ %H:%M:%S')
    username            = serializers.SerializerMethodField()
    email               = serializers.SerializerMethodField()
    title               = serializers.SerializerMethodField()
    frequency           = serializers.SerializerMethodField()
    frequency_value     = serializers.SerializerMethodField()
    type                = serializers.SerializerMethodField()
    trial_type          = serializers.SerializerMethodField()

    def get_username(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.username

    def get_email(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.email

    def get_title(self, obj):
        subscription = Subscription.objects.get(id=obj.subscription_id)
        return subscription.title

    def get_frequency(self, obj):
        subscription = Subscription.objects.get(id=obj.subscription_id)
        return subscription.frequency

    def get_frequency_value(self, obj):
        subscription = Subscription.objects.get(id=obj.subscription_id)
        return subscription.frequency_value

    def get_type(self, obj):
        subscription = Subscription.objects.get(id=obj.subscription_id)
        return subscription.type

    def get_trial_type(self, obj):
        subscription = Subscription.objects.get(id=obj.subscription_id)
        return subscription.trial_type

    class Meta:
        model = UserSubscriptionIntent
        fields = ('user_id', 'subscription_id', 'signup_date', 'notified', 'username', 'email', 'title', 'frequency', 'frequency_value', 'type', 'trial_type')
        