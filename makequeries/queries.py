from requests.models import BasicInformation
from django.contrib.auth.models import User

print('User basicinformation count==')
for i in BasicInformation.objects.all():
    print(i.user.username + ' ' + str(i.age) + ' ' + str(i.address) + ' ' + str(i.contact_number))
print('=============================')

print('Total users==================')
print(BasicInformation.objects.count())
print('=============================')

print('User=========================')
for i in User.objects.all():
    print(str(i))
print('=============================')
