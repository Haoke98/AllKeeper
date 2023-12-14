from django.db import models

from .service import Service


class ElasticSearch(Service):
    elasticPwd = models.CharField(max_length=36, verbose_name="elastic", null=True,
                                  blank=False)
    kibanaPwd = models.CharField(max_length=36, verbose_name="kibana_system", null=True,
                                 blank=True)
    apmPwd = models.CharField(max_length=36, verbose_name='apm_system',
                              null=True, blank=True)
    logstashPwd = models.CharField(max_length=36,
                                   verbose_name='logstash_system',
                                   null=True, blank=True)
    beatsPwd = models.CharField(max_length=36,
                                verbose_name='beats_system', null=True, blank=True)
    remoteMonitoringPwd = models.CharField(max_length=36,
                                           verbose_name='remote_monitoring_user', null=True, blank=True)

    class Meta:
        verbose_name = "ElasticSearch弹性检索引擎"
        verbose_name_plural = verbose_name
