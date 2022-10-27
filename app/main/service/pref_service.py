from main.model.music_pref import Music_pref
from main.model.smoking_pref import Smoking_pref
from main.model.speaking_pref import Speaking_pref


def getAllMusicPref():
    return Music_pref.query.all()


def getAllSpeakingPref():
    return Speaking_pref.query.all()


def getAllSmokingPref():
    return Smoking_pref.query.all()


def getMusicPrefById(music_pref_id):
    return Music_pref.query.filter_by(id=music_pref_id).first()


def getSmokingPrefById(smoking_pref_id):
    return Smoking_pref.query.filter_by(id=smoking_pref_id).first()


def getSpeakingPrefById(speaking_pref_id):
    return Speaking_pref.query.filter_by(id=speaking_pref_id).first()
