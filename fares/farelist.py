import httplib, json

def parse_fare(type_, data):
	if type_ is "trip-specific":
		return _fare_trip_specific(data)
	if type_ is "per_vehicle":
		return _fare_per_vehicle(data)
	if type_ is "one_fare":
		return _fare_one_fare(data)

def _fare_trip_specific(data):
	raise NotImplementedError("Per Vehicle Only")

def _fare_per_vehicle(data):
	raise NotImplementedError("Per Vehicle Only")

def _fare_one_fare(data):
	h = httplib.HTTPConnection(_urls[data['city']][0])
	h.request("POST", _urls[data['city']][1], 
		'{"AgencyId":"' + _cities[data['city']] + '"}', 
		{'Content-type':'application/json',
		 'Accept':'text/plain'}
	)
	r = h.getresponse()
	for blob in json.loads(r.read()):
		if "single" not in blob["TicketTypeDescriptionEn"].lower():
			continue 
		if data['type'] in ["metro", "subway"] and blob["Subway"] is True:
			return blob["Price"]
		if data['type'] in ["bus"] and blob["Bus"] is True:
			return blob["Price"]


_urls = {
	"Laval":["50.21.160.24:8001", "/API/Fares/"]
}

_cities = {
	"Laval":"STL"
}

if __name__ == '__main__':
	print parse_fare("one_fare", {'city':"Laval", "type":'subway'})