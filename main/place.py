class Place(object):
	rating = 0.0
	name = ''
	price_level = 0
	longitude = 0.0
	latitude = 0.0
	vicinity = ''

	def __init__(self, rating, name, price_level, latitude, longitude, vicinity):
		self.rating = rating
		self.name = name
		self.price_level = price_level
		self.latitude = latitude
		self.longitude = longitude
		self.vicinity = vicinity

def make_place(rating, name, price_level, latitude, longitude, vicinity):
	place = Place(rating,name, price_level, latitude, longitude, vicinity)
	return place
