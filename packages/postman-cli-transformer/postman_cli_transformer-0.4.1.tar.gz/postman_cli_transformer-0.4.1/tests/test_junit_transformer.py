from datetime import datetime
from postman_cli_transformer.junit_transformer import (
    calculate_time,
    compress,
    junit_transform,
)


def test_building_of_junit_doc_from_json():
    cli_json = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {
                                    "result": "FAILED",
                                    "error_id": "1",
                                    "details": {
                                        "type": "AssertionError",
                                        "detail": '1Region object structure is as expected\n2expected null to be a number\nxat assertion:2 in test-script\nyinside "Regions / Find if name corresponds to a known region"',
                                    },
                                },
                            },
                            {
                                "desc": "All required fields in the region object are present and not empty",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Find if name corresponds to a known region",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.83kB",
                                    "time": "2287ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {
                                    "result": "FAILED",
                                    "error_id": "2",
                                    "details": {
                                        "type": "AssertionError",
                                        "detail": '3Region object structure is as expected\n4expected null to be a number\naat assertion:2 in test-script\nbinside "Regions / Find if name corresponds to a known region"',
                                    },
                                },
                            },
                            {
                                "desc": "All required fields in the region object are present and not empty",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
        ],
        "summary": {
            "iterations": {"executed": "1", "failed": "0"},
            "requests": {"executed": "4", "failed": "0"},
            "test-scripts": {"executed": "2", "failed": "0"},
            "prerequest-scripts": {"executed": "4", "failed": "0"},
            "assertions": {"executed": "0", "failed": "2"},
            "totals": {
                "totalRunDuration": "487ms",
                "totalDataReceived": "604B (approx)",
                "responseTimes": {
                    "average": "103ms",
                    "min": "51ms",
                    "max": "253ms",
                    "s.d.": "86ms",
                },
            },
        },
    }

    current_time_of_test_run = datetime.now().isoformat()

    results = junit_transform(cli_json, current_time_of_test_run)

    expected_result = (
        '''<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Pinball Map Collection" tests="2" time="0.487">
  <testsuite name="Regions / Fetch all regions" timestamp="'''
        + current_time_of_test_run
        + '''" tests="5" failures="1" errors="0" time="0.098">
    <testcase name="Response status code is 200" time="0.098" classname="RegionsFetchAllRegions"/>
    <testcase name="Response time is within an acceptable range" time="0.098" classname="RegionsFetchAllRegions"/>
    <testcase name="Region object structure is as expected" time="0.098" classname="RegionsFetchAllRegions">
      <failure type="AssertionError" message="2expected null to be a number">
        <![CDATA[Failed 1 times.]]>
        <![CDATA[Collection name: Pinball Map Collection.]]>
        <![CDATA[Request name: Regions / Fetch all regions.]]>
        <![CDATA[Test description: 1Region object structure is as expected.]]>
        <![CDATA[Error message: 2expected null to be a number.]]>
        <![CDATA[Stacktrace: xat assertion:2 in test-script\nyinside "Regions / Find if name corresponds to a known region".]]>
      </failure>
    </testcase>
    <testcase name="All required fields in the region object are present and not empty" time="0.098" classname="RegionsFetchAllRegions"/>
    <testcase name="Region object has correct data types for fields" time="0.098" classname="RegionsFetchAllRegions"/>
  </testsuite>
  <testsuite name="Machines / Find if name corresponds to a known region" timestamp="'''
        + current_time_of_test_run
        + """" tests="5" failures="1" errors="0" time="2.287">
    <testcase name="Response status code is 200" time="2.287" classname="MachinesFindIfNameCorrespondsToAKnownRegion"/>
    <testcase name="Response time is within an acceptable range" time="2.287" classname="MachinesFindIfNameCorrespondsToAKnownRegion"/>
    <testcase name="Region object structure is as expected" time="2.287" classname="MachinesFindIfNameCorrespondsToAKnownRegion">
      <failure type="AssertionError" message="4expected null to be a number">
        <![CDATA[Failed 1 times.]]>
        <![CDATA[Collection name: Pinball Map Collection.]]>
        <![CDATA[Request name: Machines / Find if name corresponds to a known region.]]>
        <![CDATA[Test description: 3Region object structure is as expected.]]>
        <![CDATA[Error message: 4expected null to be a number.]]>
        <![CDATA[Stacktrace: aat assertion:2 in test-script\nbinside "Regions / Find if name corresponds to a known region".]]>
      </failure>
    </testcase>
    <testcase name="All required fields in the region object are present and not empty" time="2.287" classname="MachinesFindIfNameCorrespondsToAKnownRegion"/>
    <testcase name="Region object has correct data types for fields" time="2.287" classname="MachinesFindIfNameCorrespondsToAKnownRegion"/>
  </testsuite>
</testsuites>"""
    )

    assert results == expected_result


def test_time_conversion():
    time = "87ms"
    time2 = "3486ms"

    assert calculate_time(time) == 0.087 and calculate_time(time2) == 3.486


def test_invalid_time_conversion():
    time = "craig"

    assert calculate_time(time) == 0


def test_folder_name_compression():
    line = "Regions / Fetch all regions"

    assert compress(line) == "RegionsFetchAllRegions"
