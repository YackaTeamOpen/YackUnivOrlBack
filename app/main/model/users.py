from flask_login import UserMixin

class Users(UserMixin):

	photo = ""

	def __init__(self, id, type, password, name, surname, gender, email, address_id, phone, organization_id, speaking_id, music_pref_id, smoking_pref_id, points,review_id,gift_id,creation_date,last_login,unsubscribe):

		self.id = id
		self.type = type
		self.password_hash = password
		self.name = name
		self.surname = surname
		self.gender = gender
		self.email = email
		self.addresses_id = [address_id]
		self.phone = phone
		self.organization_id = organization_id
		self.speaking_id = speaking_id
		self.music_pref_id = music_pref_id
		self.smoking_pref_id = smoking_pref_id
		self.points = points
		self.reviews_id = [review_id]
		self.gifts_id = [gift_id]
		self.creation_date = creation_date
		self.last_login = last_login
		self.unsubscribe = unsubscribe
		
	def __repr__(self):
		return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
      self.id,
      self.type,
      self.password_hash,
      self.name,
      self.surname,
      self.gender,
      self.email,
      self.addresses_id,
      self.phone,
      self.organization_id,
      self.speaking_id,
      self.music_pref_id,
      self.smoking_pref_id,
      self.points,
      self.reviews_id,
      self.gifts_id,
      self.creation_date,
      self.last_login,
      self.unsubscribe
      )
