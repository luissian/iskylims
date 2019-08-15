from django.db import models
from django.contrib.auth.models import User
import datetime





class Laboratory (models.Model):
    labName = models.CharField(max_length=50)
    labCoding = models.CharField(max_length=10)
    labLocation = models.CharField(max_length=255)

    def __str__ (self):
        return '%s' %(self.labName)

    def get_name(self):
        return '%s' %(self.labName)

    def get_lab_code (self):
        return '%s' %(self.labCoding)


class MoleculeType (models.Model):
    moleculeType = models.CharField(max_length = 30)

    def __str__ (self):
        return '%s' %(self.moleculeType)

    def get_name (self):
        return '%s' %(self.moleculeType)


class ProtocolType (models.Model):
    molecule = models.ForeignKey(
                    MoleculeType,
                    on_delete= models.CASCADE, null = True, blank = True)
    protocol_type = models.CharField(max_length = 40)

    def __str__ (self) :
        return '%s' %(self.protocol_type)

    def get_name (self):
        return '%s' %(self.protocol_type)

class Protocols (models.Model):
    type =  models.ForeignKey(
                    ProtocolType,
                    on_delete= models.CASCADE)
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length = 160, null = True, blank = True)

    def __str__ (self) :
        return '%s' %(self.name)

    def get_name (self):
        return '%s' %(self.name)

class ProtocolParameters (models.Model):
    protocol_id = models.ForeignKey(
                    Protocols,
                    on_delete= models.CASCADE)
    parameterName = models.CharField(max_length=255)
    parameterDescription = models.CharField(max_length= 400, null=True, blank=True)
    parameterOrder = models.IntegerField()
    parameterUsed = models.BooleanField()
    parameterMaxValue = models.CharField(max_length = 50, null = True, blank = True)
    parameterMinValue = models.CharField(max_length = 50, null = True, blank = True)





class StatesForSample (models.Model):
    sampleStateName = models.CharField(max_length=50)

    def __str__ (self):
        return '%s' %(self.sampleStateName)


class SampleType (models.Model):
    sampleType = models.CharField(max_length=50)

    def get_name(self):
        return '%s' %(self.sampleType)


class Species (models.Model):
    spicesName = models.CharField(max_length=50)
    refGenomeName = models.CharField(max_length=255)
    refGenomeSize = models.CharField(max_length=100)
    refGenomeID = models.CharField(max_length=255)

    def __str__ (self):
        return '%s' %(self.spicesName)

    def get_name(self):
        return '%s' %(self.spicesName)

class SamplesManager (models.Manager):

    def create_sample (self, sample_data):
        new_sample = self.create(sampleState = StatesForSample.objects.get(sampleStateName__exact = 'Defined'),
                            laboratory = Laboratory.objects.get(labName__exact = sample_data['laboratory']),
                            patientCodeName = sample_data['patientCodeName'],
                            sampleType = SampleType.objects.get(sampleType__exact = sample_data['sampleType']) ,
                            sampleUser = User.objects.get(username__exact = sample_data['user']),
                            sampleCodeID = sample_data['sample_id'] , sampleName =  sample_data['sampleName'],
                            uniqueSampleID = sample_data['new_unique_value'],
                            species = Species.objects.get(spicesName__exact = sample_data['species']),
                            sampleExtractionDate = datetime.datetime.strptime(sample_data['extractionDate'],'%Y-%m-%d %H:%M:%S'))
        return new_sample

class Samples (models.Model):
    sampleState = models.ForeignKey(
                StatesForSample,
                on_delete = models.CASCADE, null = True)
    laboratory = models.ForeignKey(
                Laboratory,
                on_delete = models.CASCADE, null = True)
    sampleType = models.ForeignKey(
                SampleType,
                on_delete = models.CASCADE, null = True)


    sampleUser = models.ForeignKey(
                User,
                on_delete=models.CASCADE, null = True)

    species = models.ForeignKey(
                Species,
                on_delete=models.CASCADE, null = True)
    sampleName = models.CharField(max_length=255, null = True)
    labSampleName = models.CharField(max_length=255, null = True, blank = True)
    sampleExtractionDate = models.DateTimeField(auto_now_add = False, null =True)
    uniqueSampleID = models.CharField(max_length=8, null = True)
    patientCodeName = models.CharField(max_length=255, null = True)
    sampleCodeID = models.CharField(max_length=60, null = True)
    reused = models.BooleanField(null = True, blank = True)
    generated_at = models.DateTimeField(auto_now_add=True)



    def get_info_in_defined_state(self):
        sample_info = []
        sample_info.append(self.sampleExtractionDate.strftime("%d , %B , %Y"))
        sample_info.append(self.sampleCodeID)
        sample_info.append(self.patientCodeName)
        sample_info.append(self.laboratory.get_name())
        sample_info.append(self.labSampleName)
        sample_info.append(self.sampleType.get_name())
        sample_info.append(self.species.get_name())
        sample_info.append(str(self.pk))
        return sample_info

    def get_full_definition_info (self):
        recordeddate=self.sampleExtractionDate.strftime("%B %d, %Y")

        return '%s;%s;%s;%s;%s' %(self.registerUser)

    def get_sample_code (self):
        return '%s' %(self.sampleCodeID)

    def get_sample_id(self):
        return '%s' %(self.id)

    def get_sample_nucleic_accid (self):
        return '%s' %(self.nucleicAccid)

    def get_sample_protocol (self):
        return '%s' %(self.sampleProtocol)

    def get_register_user(self):
        if self.sampleUser is None:
            return 'Not avilable'
        else:
            return '%s' %(self.sampleUser)

    def get_registered_sample (self):
        recordeddate=self.generated_at.strftime("%B %d, %Y")
        return '%s' %(recordeddate)

    objects = SamplesManager()
