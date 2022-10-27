class Path_point :
    """ définition d'un élément d'itinéraire, composé de champs d'adresse et de géocoordonnées """
    # Rq : le nom path_point n'est pas satisfaisant non plus (voir rq pour l'objet path)

    def __init__(self, street, city, zipcode, latitude, longitude) :
        self.street = street
        self.city = city
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) :
        return self.street + " " + self.zipcode + " " + self.city + " ; [" + repr(self.latitude) + ", " + repr(self.longitude) + "]"


class Path :
    """ définition d'un objet itinéraire (en qq sorte un Trip réduit aux infos de localisation et d'horaire...) """
    # Rq : le nom path n'est pas satisfaisant, il vaudrait mieux un nom signifiant simplement
    # un départ, une arrivée et éventuellement un point d'étape. Car le mot path peut se comprendre
    # comme un ensemble de points successifs non limité à 2 ou 3, comme d'ailleurs il le  signifie
    # dans le dictionnaire retourné par path_matching.

    def __init__(self, trip_id, start_point, arrival_point, start_time, arrival_time, waypoint) :
        self.trip_id = trip_id
        self.start_point = start_point
        self.arrival_point = arrival_point
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.waypoint = waypoint

    def __repr__(self) :
        return repr(self.trip_id) + "\n" + repr(self.start_point) + "\n" + repr(self.arrival_point) + "\n" + repr(self.start_time) + "\n" + repr(self.arrival_time) + "\n" + repr(self.waypoint)
