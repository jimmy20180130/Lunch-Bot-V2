import json
from others import load_lunch, save_lunch, error_info

def add_money(id: int, money: int):
    try:
        if not (int(money) <= 0):
            user_data = load_lunch()
            if user_data['now'][str(id)]['wallet'] == '':
                user_data['now'][str(id)]['wallet'] = int(money)
            else:
                user_data['now'][str(id)]['wallet'] = int(user_data['now'][str(id)]['wallet']) + int(money)
            save_lunch(user_data)
            return user_data['now'][str(id)]['wallet']
        else:
            return 'error, value<=0'
    except Exception as e:
        err_msg = error_info(e)
        return f'error, {err_msg}'

def set_money(id :int, money :int):
    try:
        if not (int(money) <= 0):
            user_data = load_lunch()
            user_data['now'][str(id)]['wallet'] = int(money)
            save_lunch(user_data)
            return user_data['now'][str(id)]['wallet']
        else:
            return 'error, value<=0'
    except Exception as e:
        err_msg = error_info(e)
        print(err_msg)
        return f'error, {err_msg}'

def remove_money(id :int, money :int):
    try:
        if not (int(money) <= 0):
            user_data = load_lunch()
            if not (user_data['now'][str(id)]['wallet'] == '' or user_data['now'][str(id)]['wallet'] is None or (int(user_data['now'][str(id)]['wallet']) < money)):
                user_data['now'][str(id)]['wallet'] = int(user_data['now'][str(id)]['wallet']) - int(money)
                save_lunch(user_data)
                return user_data['now'][str(id)]['wallet']
            else:
                return 'error, wallet<money'
        else:
            return 'error, value<=0'
    except Exception as e:
        err_msg = error_info(e)
        print(err_msg)
        return f'error, {err_msg}'
    
def add_all_money(money: int):
    try:
        if not (int(money) <= 0):
            user_data = load_lunch()
            for user_id in user_data['now']:
                if user_data['now'][user_id]['wallet'] != '':
                    user_data['now'][user_id]['wallet'] = int(user_data['now'][user_id]['wallet']) + int(money)
                else:
                    user_data['now'][user_id]['wallet'] = int(money)
            save_lunch(user_data)
        else:
            return 'error, value<=0'
    except Exception as e:
        err_msg = error_info(e)
        print(err_msg)
        return f'error, {err_msg}'

def set_all_money(money: int):
    try:
        if not (int(money) <= 0):
            user_data = load_lunch()
            for user_id in user_data['now']:
                user_data['now'][user_id]['wallet'] = int(money)
            save_lunch(user_data)
        else:
            return 'error, value<=0'
    except Exception as e:
        err_msg = error_info(e)
        print(err_msg)
        return f'error, {err_msg}'

def remove_all_money(money: int):
    try:
        if not (int(money) <= 0):
            user_data = load_lunch()
            for user_id in user_data['now']:
                if user_data['now'][user_id]['wallet'] != '':
                    user_data['now'][user_id]['wallet'] = int(user_data['now'][user_id]['wallet']) - int(money)
                else:
                    user_data['now'][user_id]['wallet'] = int(money)
            save_lunch(user_data)
        else:
            return 'error, value<=0'
    except Exception as e:
        err_msg = error_info(e)
        print(err_msg)
        return f'error, {err_msg}'