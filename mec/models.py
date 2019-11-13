from django.contrib.gis.db import models

class Election(models.Model):
    date = models.DateField()
    TYPE_CHOICES = (
        ('GE','General'),
        ('PR','Primary'),
        ('MG','Municipal General'),
        ('MP','Municipal Primary'),
        ('SE','Special Election')
    )
    type = models.CharField(max_length=2,choices=TYPE_CHOICES)

    def __str__(self):
        return self.date.__str__() + ' (' + self.get_type_display() + ')'

class District(models.Model):
    name = models.CharField(max_length=25)
    number = models.IntegerField()
    district_type = models.CharField(max_length=2)
    boundaries = models.PolygonField()

    def __str__(self):
        return self.name


class Address(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    districts = models.ManyToManyField(District)
    us_h_dist = models.ForeignKey(District, related_name='us_h_dist', null=True, on_delete=models.CASCADE)
    mo_h_dist = models.ForeignKey(District, related_name='mo_h_dist', null=True, on_delete=models.CASCADE)
    mo_s_dist = models.ForeignKey(District, related_name='mo_s_dist', null=True, on_delete=models.CASCADE)

    coordinates = models.PointField(null=True)

    def __str__(self):
        return self.address1 + ", " + \
            self.city + ", " + self.state + ' ' + self.zip

class Committee(models.Model):
    MECID = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)

class Individual(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Contributor(models.Model):
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
    committee = models.OneToOneField(Committee, null=True, blank=True, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, null=True, blank=True, on_delete=models.CASCADE)
    individual = models.OneToOneField(Individual, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.committee:
            return self.committee.name
        elif self.company:
            return self.company.name
        elif self.individual:
            return self.individual.first_name + " " +  self.individual.last_name

class Contribution(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField()
    donation_type = models.CharField(max_length=10,choices=(
        ('M','Monetary'),
        ('I','In-Kind'),
    ))
    report = models.CharField(max_length=100)
    recipient = models.ForeignKey(Committee, null=True, blank=True, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + ' ' + str(self.date) + ' ' + str(self.contributor)


# class Candidate(models.Model):
#     committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
#     candidate_name = models.CharField(max_length=50)
#     current_party = models.CharField(max_length=1)
#     election = models.ManyToManyField(Election,through='Campaign')

#     def __str__(self):
#         return self.candidate_name #+ ' (' + current_party + ')'

# class Campaign(models.Model):
#     candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
#     election = models.ForeignKey(Election, on_delete=models.CASCADE)
#     office_sought = models.CharField(max_length=200)
#     party = models.CharField(max_length=1)