from django.db import models

# Create your models here.
class SbrCurrentsessions(models.Model):
    sbr_uniquesessionid = models.CharField(db_column='Sbr_UniqueSessionId', primary_key=True, max_length=16)  # Field name made lowercase.
    sbr_creationtime = models.DateTimeField(db_column='Sbr_CreationTime')  # Field name made lowercase.
    sbr_expirationtime = models.DateTimeField(db_column='Sbr_ExpirationTime')  # Field name made lowercase.
    sbr_ipv4address = models.PositiveIntegerField(db_column='Sbr_Ipv4Address', blank=True, null=True)  # Field name made lowercase.
    sbr_ippoolordinal = models.PositiveSmallIntegerField(db_column='Sbr_IpPoolOrdinal', blank=True, null=True)  # Field name made lowercase.
    sbr_nasname = models.CharField(db_column='Sbr_NasName', max_length=39)  # Field name made lowercase.
    sbr_sessionstate = models.PositiveIntegerField(db_column='Sbr_SessionState')  # Field name made lowercase.
    sbr_userconcurrencyid = models.CharField(db_column='Sbr_UserConcurrencyId', max_length=84, blank=True, null=True)  # Field name made lowercase.
    sbr_mobileiptype = models.PositiveIntegerField(db_column='Sbr_MobileIpType', blank=True, null=True)  # Field name made lowercase.
    sbr_3gpp2reqtype = models.PositiveIntegerField(db_column='Sbr_3gpp2ReqType', blank=True, null=True)  # Field name made lowercase.
    sbr_wimaxclienttype = models.PositiveIntegerField(db_column='Sbr_WimaxClientType')  # Field name made lowercase.
    sbr_wimaxacctflows = models.CharField(db_column='Sbr_WimaxAcctFlows', max_length=2047, blank=True, null=True)  # Field name made lowercase.
    sbr_3gpp2homeagentaddr = models.PositiveIntegerField(db_column='Sbr_3gpp2HomeAgentAddr', blank=True, null=True)  # Field name made lowercase.
    sbr_acctautostop = models.CharField(db_column='Sbr_AcctAutoStop', max_length=1023, blank=True, null=True)  # Field name made lowercase.
    sbr_classattribute = models.CharField(db_column='Sbr_ClassAttribute', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    sbr_username = models.CharField(db_column='Sbr_UserName', max_length=24, blank=True, null=True)  # Field name made lowercase.
    sbr_acctsessionid = models.CharField(db_column='Sbr_AcctSessionId', max_length=24, blank=True, null=True)  # Field name made lowercase.
    sbr_transactionid = models.CharField(db_column='Sbr_TransactionId', max_length=12, blank=True, null=True)  # Field name made lowercase.
    sbr_nasporttype = models.PositiveIntegerField(db_column='Sbr_NasPortType', blank=True, null=True)  # Field name made lowercase.
    sbr_nasport = models.PositiveIntegerField(db_column='Sbr_NasPort', blank=True, null=True)  # Field name made lowercase.
    sbr_callingstationid = models.CharField(db_column='Sbr_CallingStationId', max_length=24, blank=True, null=True)  # Field name made lowercase.
    sbr_calledstationid = models.CharField(db_column='Sbr_CalledStationId', max_length=24, blank=True, null=True)  # Field name made lowercase.
    sbr_mobilecorrelationid = models.CharField(db_column='Sbr_MobileCorrelationId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    sbr_ipv6interfaceid = models.CharField(db_column='Sbr_Ipv6InterfaceId', max_length=16, blank=True, null=True)  # Field name made lowercase.
    sbr_nasipv4address = models.PositiveIntegerField(db_column='Sbr_NasIpv4Address', blank=True, null=True)  # Field name made lowercase.
    sbr_nasipv6address = models.CharField(db_column='Sbr_NasIpv6Address', max_length=16, blank=True, null=True)  # Field name made lowercase.
    wimaxsessionid = models.CharField(db_column='WimaxSessionId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    acctmultisessionid = models.CharField(db_column='AcctMultiSessionId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    funkouterusername = models.CharField(db_column='FunkOuterUserName', max_length=84, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sbr_CurrentSessions'
