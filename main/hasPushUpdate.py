import random
import datetime
def has_push_update(patch_type, request, patch_monitoring, create_time, user_count=None):
    kwarg_list = []
    time_condition = {}
    user_count = 10 if user_count == None else user_count
    patchType, other = patch_type.split(':')
    flag = True
    if patchType == "condition":
        condition_list = other.split("&")
        if '' in condition_list:condition_list.remove('')
        temp_list = list()
        for i in condition_list:
            j = i.split('=')
            if j[0] == 'week':
                time_condition[j[0]]=j[1]
            else:  
                temp_list.append(tuple(j))
        temp_dict = dict(temp_list)
        request_dict = request.GET
        for i in temp_dict:
            flag = i in request_dict
        if time_condition:
            for i in time_condition:
                if i == "week":
                    days = int(time_condition[i])*7
                    create_time += datetime.timedelta(days=days)
                    flag = datetime.datetime.now() < create_time
                
    elif patchType == "gray":
        if "&" in other:
            other, time_out = other.split("&")
        gray_type, gray_value = other.split("=")
        time_key, time_value = time_out.split("=")
        days = int(time_value)*7
        create_time += datetime.timedelta(days=days)
        flag = datetime.datetime.now() <= create_time
        success_count = 0
        for i in patch_monitoring:
            success_count += i.success_count
        print(success_count)        
        if gray_type == "percentage":
            percentage_value = success_count/user_count
            flag = percentage_value <= (int(gray_value)/10)
            flag = (random.randint(1,100)/10) <= int(gray_value)
        else:
            flag = success_count <= int(gray_value)
    elif patchType == "private":
        pass
    return flag