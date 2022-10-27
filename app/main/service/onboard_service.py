from main.service.user_service import update_user, update_last_login


def onboard_user(user_id, data):

    # Enregistrement des informations personnelles
    user_datas = {
        "photo": data["photo"],
        "name": data["name"],
        "surname": data["surname"],
        "phone": data["phone"],
        "aboutme": data["aboutme"],
        "speaking_pref_id": int(data["speaking_pref_id"]),
        "smoking_pref_id": int(data["smoking_pref_id"]),
        "music_pref_id": int(data["music_pref_id"]),
        # "public_phone":bool(data["public_phone"]),
        "gender": data["gender"]
    }

    result_update_user = update_user(user_id, user_datas)
    update_last_login(user_id)
    return result_update_user
