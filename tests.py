# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/3/1
@Software: PyCharm
@disc:
======================================="""
import io

import requests
import matplotlib.pyplot as plt
import urllib.request

from PIL import Image





if __name__ == '__main__':
    # cap = cv2.VideoCapture('/Users/shadikesadamu/Documents/001.mp4')
    # success, img = cap.read()
    # if success:
    #     thumbnail = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #     thumbnail.thumbnail((200, 200))
    #     thumbnail.show()
    resp = requests.get(
        "https://tvax4.sinaimg.cn/crop.0.0.1080.1080.180/007l7TJEly8h28dlo82muj30u00u077m.jpg?KID=imgbed,tva&Expires=1688620922&ssig=zAZm5C9ajZ",
        headers={
            "referer": "https://weibo.com/"
        }
    )
    with open("test1.jpg", 'wb') as f:
        f.write(resp.content)
    resp = requests.get(
        "https://www.douyin.com/user/MS4wLjABAAAAce0znIM0dAXCkfi2sb40HUoRHTKn620uv1-TfvoJyrW_eZ8UFAWrJAECXzZ4-Wpx",
        headers={
            "Cookie": "douyin.com; webcast_local_quality=null; ttwid=1%7CFVsI8p5NqSV0-tGsXXqTGM9W1lChTpzNWSvJX3qcwy4%7C1672334140%7C4beac5b46058d5a4610136531f6614f094e7e78e61a951d110f49196cfb85827; passport_assist_user=CjzdyEf6aNOx2V2PA_t_PwvIedrWboy-znlRnhVzO5zm_OQVxVMQ-biUI0FFQ9Wx1ayC6lRxHM9uQwHaZt8aSAo8oOj5sifMvgJOZbEOEgKYqUHXdWNQvd8EY1nj04HZy5PAB8_X8CrrJuwk1BW-SCQkpOD9Dnym36MOg0bqEJ2XpQ0Yia_WVCIBAzr0U78%3D; sso_uid_tt=fad2d60aaed386e6fade404c6e06cbaa; sso_uid_tt_ss=fad2d60aaed386e6fade404c6e06cbaa; toutiao_sso_user=bd2f9bfd556bd087d3ae542113d302b7; toutiao_sso_user_ss=bd2f9bfd556bd087d3ae542113d302b7; uid_tt=95c8a60f02b33b171464e58c4c5ed44a; uid_tt_ss=95c8a60f02b33b171464e58c4c5ed44a; sid_tt=4f0131a1aaa13413632ce54ee60a1e35; sessionid=4f0131a1aaa13413632ce54ee60a1e35; sessionid_ss=4f0131a1aaa13413632ce54ee60a1e35; store-region=cn-xj; store-region-src=uid; LOGIN_STATUS=1; my_rd=1; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEakNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRU1jQ2NiZU8yMU5PTS9EaFVjNVR3dUh6NFxyXG51b1NQOFlmdStLZ1BLY1AvTVlRb0N4R1owL2YzSTg3dVZUam9TNkI2bUh3NUMvRDRnRDcrY0dGMmlicXRMNkFzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU0FBd1JRSWhBSWZJSFhNWWc0MitKUjJob2w1ZG1IQ2pYV0dJaUM1eHVnZ005WElLMjV2RlxyXG5BaUFDekhQaDZocEdwVGpFbVJ1Z1hqUWlIc3FUZXRpY2RvUlNNcFRVUXdPaktnPT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; __live_version__=%221.1.1.93%22; passport_csrf_token=52d29de623b6988ff2df7396e879a3e7; passport_csrf_token_default=52d29de623b6988ff2df7396e879a3e7; pwa2=%220%7C1%7C1%7C0%22; douyin.com; device_web_cpu_core=10; device_web_memory_size=8; webcast_local_quality=null; csrf_session_id=9975e26ea6c5a688fb8694322f16038f; sid_ucp_sso_v1=1.0.0-KGRlMmE1Zjc3NTMzOGJhOGI2OTE2NmY1NDlhMTdjYzJjNGQ4MGUxNzIKHQjXoqDE7AEQoMPfpAYY7zEgDDC41Z3LBTgGQPQHGgJsZiIgYmQyZjliZmQ1NTZiZDA4N2QzYWU1NDIxMTNkMzAyYjc; ssid_ucp_sso_v1=1.0.0-KGRlMmE1Zjc3NTMzOGJhOGI2OTE2NmY1NDlhMTdjYzJjNGQ4MGUxNzIKHQjXoqDE7AEQoMPfpAYY7zEgDDC41Z3LBTgGQPQHGgJsZiIgYmQyZjliZmQ1NTZiZDA4N2QzYWU1NDIxMTNkMzAyYjc; sid_guard=4f0131a1aaa13413632ce54ee60a1e35%7C1687675296%7C5184000%7CThu%2C+24-Aug-2023+06%3A41%3A36+GMT; sid_ucp_v1=1.0.0-KGIxNDUwZjNlMjNkZDMxNTNlYTQyMTNiYzlkMmU4OWE3NDlkMmVmMzcKFwjXoqDE7AEQoMPfpAYY7zEgDDgGQPQHGgJobCIgNGYwMTMxYTFhYWExMzQxMzYzMmNlNTRlZTYwYTFlMzU; ssid_ucp_v1=1.0.0-KGIxNDUwZjNlMjNkZDMxNTNlYTQyMTNiYzlkMmU4OWE3NDlkMmVmMzcKFwjXoqDE7AEQoMPfpAYY7zEgDDgGQPQHGgJobCIgNGYwMTMxYTFhYWExMzQxMzYzMmNlNTRlZTYwYTFlMzU; publish_badge_show_info=%220%2C0%2C0%2C1688349839809%22; strategyABtestKey=%221688349839.819%22; SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%223%2F20230703%2F1%22; __bd_ticket_guard_local_probe=1688354462819; odin_tt=7c30a9e10419d87cf2977acfc045bfa4a0a49e7f95aa98d88c71260c3dd48861a4456c96b2d70a58634c8b0bf90b22d7; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1688969059949%2C%22type%22%3A1%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA8LONkHj2UXKiDftrVJFveNOXaqRfMN6L6JDd-usaisc%2F1688400000000%2F0%2F0%2F1688365518303%22; __ac_nonce=064a2a474005a4b52545c; __ac_signature=_02B4Z6wo00f010Xnz8gAAIDA0TGUxDv96q9Fx8tAALXmdmZ6L3yoIJmFnbPXXyHbZjm2Q1TNtozpuxWvWZONiy.WoGPXPL.DlJ7uBknbpnvbM0jefj7wyQq6BMIM3MigrAz5LQKcjKpa0iH1ff; msToken=gEUz1nUuwvgCvl4epLDpgQQIwmRwSUrvBoKc9YsMjasXuaiiaPgNbXotTzl-qtEtIq-gYC0IJttePBxiZ7Xnt1DMLjWbjaS_064kpc7bpqB5GKZXFcITOG4=; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA8LONkHj2UXKiDftrVJFveNOXaqRfMN6L6JDd-usaisc%2F1688400000000%2F0%2F1688381596133%2F0%22; home_can_add_dy_2_desktop=%221%22; msToken=p8pYgNnBv3r110UEJ5HY7tyjgN1zakvkDsVYZwKr6JyoSVMx3UGRNxUdTQKDjiqU4_-ukNQwLKsJpHOSpOVswHMwsfL_Zp7FI2GI2qn9IGMEvQkXjjGWnbM=; tt_scid=FR.-xn183Acl6rmne.mAfKFEDCyyKW0QMTcm1MpL6cM97HlZ8a.t1y0yFHkt52KX3beb; passport_fe_beating_status=false"
        })
    with open("dy-test.html", "wb") as f:
        f.write(resp.content)
