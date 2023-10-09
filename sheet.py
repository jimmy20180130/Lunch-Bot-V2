import pygsheets
import json
import base64
from others import error_info, load_lunch, save_lunch, load_lunch_data
import time as t
import copy

def load_sheet():
    try:
        # 要解碼的 Base64 字串
        encoded_data = 'ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiZmx1ZW50LWNvZGVyLTM5NjYxNCIsCiAgInByaXZhdGVfa2V5X2lkIjogIjdiYThkNzk2NTQzNGQ3NzAxNTIwNjVhOWU0ODBhYWM0OTFlMjVkMjAiLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2Z0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktnd2dnU2tBZ0VBQW9JQkFRQzV4cXEvUzMra0toU0hcbnM1ajBUYjBMeFNEcmVGeFVXTVVBNVdhNUE0S0x0OWdaTVYxd2RNNEdnUHE4RmtDVEhFUmJPMGN4ZEw2NTI4MzZcbjFQSmJaOHlmaDV3RWpTYU81ZC9LeW80VlplbTdhcjA3TkNHWXhBbzcrd3NNN2lTWUlKaXg5ZlBtQWxhMDk2eUhcblZ3eGo3ZEdqOUQreWo3WmNjTzBnUWpQbDNvSkFKYis3dURJeEVNWTZUdUxvOC8zK0N1UEoxSDhvYTRXdk1VWE1cbnVMMkR5RWtnQTFFTDRSQWdrVWZ5NFFPcE00bTRtZ1VkdS9TS2ZxcEtZUXVWSmoxUTdkbGhQdENYN2RlaXE5a0lcbno3a1dURFpSUnlMMU5YK3lFTG9FajlmMFdaMTh0eDd4bktHUzdFeHNkelhZRHZ5bm5lMmVIZGtSY01VWkNMMk9cbjYzN2E2WTB4QWdNQkFBRUNnZ0VBVXllNUVDMWtNZ0JmOWlvTzRmUFdGZW1rQmFKM2VZM09pTXNtUXRSdVg4bm5cbjRjYjE4enRsYVFYY3Rjb2tGM1ZFcDYyTi9YWXJWUmd0U0FSL2d5aWdNQnhNV3NFdnJERDdEbFBDYTVPVm5yMTFcbmZJV21NREkzL29jdGVCazBxaCtWR2J0azgrVENHUGp2OGhpbHhDa1VlSllBMlJWNDVFSHI4aytQMlduUzFaRU1cbmhEVGRObzl6TjZlRmsrcmp2Z1Y2ZFp5Q3R2SEdSVkI5ZGJBOGJ4cERBWE40WjFhT0RPZGZ5VG1QM2l0d2s0dlhcbmw5VXdyN05GR3l6ZjROcGp1SDgrTVpKV3B3SVVRbFFBNmE5Z1F5UjlvSG8zanY1WlJQbm9MNEJMVCtOTlYrVkRcbmtNNmFtUUxuZTlMajZZNnJTekl2NUVFdkNBVGN1bFozNlB5bDNtbWkvUUtCZ1FEbkxYNUV6V2lqdTNvcTVLODhcblFhTStiSWFJQlFwc2l5VGkyTHhUV205aUdwMGdJMTFxTDdveHBCbVpiSVJyUjNxL0VTNmpwZ2lsVm9rMWRKZzdcbllNYkg3MFpYaDhXNHl6cnlWMDNnaGlGY1RMcW5XUmJVbnYvVi9DNngzZEtiV3diajl3a0JBMjlkQkR5eE9vSm9cbjlobXkybWlxakRwN2hGOUpJVWx6akgwSGJ3S0JnUUROdVRHUU9pd3d0ZDk4VWxvSkh5d3ZyS1BUUnFHV1UxMzNcblp4aEhPYXREeWd0U0JQSktwNW56Tms1WS9JNllyOHRTSVRYTzNVbTVVb2RnQlhibkhPdloxdnkwRkV1cGpOVmhcbkVCN1MzQ3ZKazZrWS90UkZLMGYvdWx1Z1dUckFjWVFCL2dvckRzeHd4bmM5d2tIeVk0d2I2NUl0RmwvTFQ2elBcbi9GSFVNanRsWHdLQmdRREVkZTM3N0pDRHJOeWF2VE9Ld3NGSFdKVlAzUERKNDhvYUdsU1poWjVvd2ZOTUQ2SGdcbmp1VHVNT1lzYzROcFpCcVZhN1cyRDNFRGliSWJRcFhveUVyR09Mc1B3ZXV2S3M5U2lnMDl4Tjl2QUNvVDgrc3FcbkVHR2M2YTZKSzlsQ2U2NDBaNGs0V2tIMnk1WUVpNU91UFk4RFp3ZFNBTS9tamswbjZlanhFTEJrY3dLQmdRQzVcbkJLNmp0UDNiVFNiU3k4bTMzSFpENWpOc3AyQmFMMTRhVEhrVVRiUlBBbDVPQks3WUg0WWdxNTJwQUhOS3RRZmFcbk5JNE5IdzNZQTNaSEVJTVFkZjFUN0x0WFJjMktqbU8xcU9iZjR5M3FXOGUvK0NkMmtlZHVBZSszOWFnV1BjRm9cbmZVNHR6V0JtcU1mREhudHJBTWFZc2JQRW94UENhVVRWeFdyZXVkS2Jad0tCZ0FFSmd6bk5NRXNFRU4weDZ0ek5cbjhoOVNBWkxmdy94QzhpMzUxd0U5bWorMnNrNVBuU1VJS3Q2aVp4Q3J1VVRUQlNoQVMrUU1ucFE3TVd2SThNMWFcbmVRNUxIWjBlUEhGN2VSODVIVnkzYUpIQzBIb2ErUXpFUmFBc3dXTWNhbzFpM2xjbnBtZHNjRGN2NnV2V0JhSVFcbjlHOWd3c3Z4bEJjNG94RncyNktNQVFkYlxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogInhpYW94aS10d0BmbHVlbnQtY29kZXItMzk2NjE0LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjExMTQwMDE5NTA3NDA4MzQ5NjcxMSIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkveGlhb3hpLXR3JTQwZmx1ZW50LWNvZGVyLTM5NjYxNC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQo='

        # 解碼 Base64 字串
        decoded_bytes = base64.b64decode(encoded_data)
        credentials = decoded_bytes.decode('utf-8')
        gc = pygsheets.authorize(service_account_json=credentials)
        spreadsheet = gc.open('lunch')
        worksheet_name = '2023/09/25-29'
        worksheet = spreadsheet.worksheet_by_title(worksheet_name)
        data = worksheet.get_all_values()

        result_json = load_lunch()
        result_json['previous'] = result_json['now']
        result_json['previous'] = copy.deepcopy(result_json['now'])
        
        for row in data[1:]:
            seat_number = row[1]
            if seat_number:
                time = row[0]
                lunch_names = row[2:7]
            
                result_json['now'][seat_number]['time'] = time
                result_json['now'][seat_number]['lunch_name'] = lunch_names
        
        sorted_new_now = dict(sorted(result_json['now'].items(), key=lambda x: int(x[0])))
        result_json['now'] = sorted_new_now
        save_lunch(result_json)

        now_data = result_json['now']
        previous_data = result_json['previous']
        
        differences = {}
        differences_list = []
        for id, now_value in now_data.items():
            previous_value = previous_data.get(id)
            if now_value != previous_value:
                differences[id] = {
                    "now": now_value,
                    "previous": previous_value
                }
        if differences != {}:
            for id, value in differences.items():
                time = value['now']['time']
                lunch_names = value['now']['lunch_name']
                previous_lunch_names = value['previous']['lunch_name']
                lunch = load_lunch_data()
                now_total_price = int(lunch[lunch_names[0]]['price'])+int(lunch[lunch_names[1]]['price'])+int(lunch[lunch_names[2]]['price'])+int(lunch[lunch_names[3]]['price'])+int(lunch[lunch_names[4]]['price'])
                before_total_price = int(lunch[previous_lunch_names[0]]['price'])+int(lunch[previous_lunch_names[1]]['price'])+int(lunch[previous_lunch_names[2]]['price'])+int(lunch[previous_lunch_names[3]]['price'])+int(lunch[previous_lunch_names[4]]['price'])
                differences_list.append({
                    id: {
                        "time": time,
                        "lunch_names": lunch_names,
                        "previous_lunch_names": previous_lunch_names,
                        "before": before_total_price,
                        "now": now_total_price
                    }
                })
                
        return differences_list
    except Exception as e:
        err_msg = error_info(e)
        print(err_msg)
        return f'error, {err_msg}'