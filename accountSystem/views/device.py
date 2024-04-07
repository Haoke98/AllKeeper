# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
import json

from django.http import HttpResponse
from rest_framework import views

from proj import esClient

INDEX_DEVICES = "devices"


class DeviceRegionView(views.View):
    def get(self, request):
        result = []
        resp = esClient.search(index=INDEX_DEVICES, size=0, aggs={
            "country": {
                "terms": {
                    "field": "geoinfo.country.code.keyword",
                    "size": 1000
                }
            }
        })
        countryBuckets: list[dict] = resp.get("aggregations").get("country").get("buckets")
        for countryBucket in countryBuckets:
            countryCode = countryBucket.get("key")
            resp1 = esClient.search(index=INDEX_DEVICES, size=1, query={
                "term": {
                    "geoinfo.country.code.keyword": {
                        "value": countryCode
                    }
                }
            }, aggs={
                "subDivisions": {
                    "terms": {
                        "field": "geoinfo.subdivisions.names.en.keyword",
                        "size": 2000
                    }
                }
            })
            country: dict = resp1.get("hits").get("hits")[0].get("_source").get("geoinfo").get("country")
            country.setdefault("doc_count", countryBucket.get("doc_count"))
            subDivisions: list[dict] = []
            subDivisionBuckets: list[dict] = resp1.get("aggregations").get("subDivisions").get("buckets")
            for subDivisionBucket in subDivisionBuckets:
                subDivisionNameEn = subDivisionBucket.get("key")
                if subDivisionNameEn == "":
                    continue
                resp2 = esClient.search(index=INDEX_DEVICES, size=1, query={
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "geoinfo.country.code.keyword": {
                                        "value": countryCode
                                    }
                                }
                            },
                            {
                                "term": {
                                    "geoinfo.subdivisions.names.en.keyword": {
                                        "value": subDivisionNameEn
                                    }
                                }
                            }
                        ]
                    }
                }, aggs={
                    "city": {
                        "terms": {
                            "field": "geoinfo.city.names.en.keyword",
                            "size": 2000
                        }
                    }
                })
                subDivision: dict = resp2.get("hits").get("hits")[0].get("_source").get("geoinfo").get("subdivisions")
                subDivision.setdefault("doc_count", subDivisionBucket.get("doc_count"))
                # TODO:统计城市City的数量
                cities: list[dict] = []
                cityBuckets: list[dict] = resp2.get("aggregations").get("city").get("buckets")
                for cityBucket in cityBuckets:
                    cityNameEn = cityBucket.get("key")
                    if cityNameEn == "":
                        continue
                    resp3 = esClient.search(index=INDEX_DEVICES, size=1, query={
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "geoinfo.country.code.keyword": {
                                            "value": countryCode
                                        }
                                    }
                                },
                                {
                                    "term": {
                                        "geoinfo.subdivisions.names.en.keyword": {
                                            "value": subDivisionNameEn
                                        }
                                    }
                                }, {
                                    "term": {
                                        "geoinfo.city.names.en.keyword": {
                                            "value": cityNameEn
                                        }
                                    }
                                }
                            ]
                        }
                    })
                    city: dict = resp3.get("hits").get("hits")[0].get("_source").get("geoinfo").get("city")
                    city.setdefault("doc_count", cityBucket.get("doc_count"))
                    cities.append(city)
                subDivision.setdefault("children", cities)
                subDivisions.append(subDivision)
            country.setdefault("children", subDivisions)
            result.append(country)
        return HttpResponse(json.dumps(result, ensure_ascii=False), headers={"content-type": "application/json"})


class DeviceView(views.View):
    def get(self, request):
        resp = esClient.search(index=INDEX_DEVICES)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), headers={"content-type": "application/json"})
