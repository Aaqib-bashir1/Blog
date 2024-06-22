from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Post, Subscription,Block
from django.core.mail import send_mail

# @receiver(post_save, sender=Post)
# def notify_subscribers(sender, instance, created, **kwargs):
#     if created:
# #         subject = 'New Post Created'
# #         message = f'A new post "{instance.title}" has been created by {instance.author.username}.'
# #     else:
# #         subject = 'Post Updated'
# #         message = f'The post "{instance.title}" by {instance.author.username} has been updated.'
# #
# #     subscribers = Subscription.objects.filter(author=instance.author).values_list('subscriber__email', flat=True)
# #     for email in subscribers:
# #         send_mail(subject, message, 'from@example.com', [email],print(message))

# @receiver(post_save, sender=Post)
# def notify_subscribers(sender, instance, created, **kwargs):
#     if created:
#         author = instance.author
#         subscribers = author.subscribers.exclude(id__in=author.blocked_by.values_list('blocker', flat=True))
#         for subscriber in subscribers:
#             send_mail(
#                 'New Post Published',
#                 f'{author.username} has published a new post: {instance.title}',
#                 'from@example.com',
#                 [subscriber.email],
#                 fail_silently=False,
#             )
#             print(f'{author.username} has published a new post: {instance.title}')
@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, **kwargs):
    author = instance.author  # Assuming Post has an author field
    subscriptions = Subscription.objects.filter(author=author)

    for subscription in subscriptions:
        subscriber = subscription.subscriber

        # Check if the author has blocked the subscriber
        if Block.objects.filter(blocker=author, blocked_user=subscriber).exists():
            continue  # Skip blocked users

        if subscriber.email:
            send_mail(
                'New Post Published',
                f'A new post has been published by {author.username}.',
                'from@example.com',
                [subscriber.email],
                fail_silently=False,
            )