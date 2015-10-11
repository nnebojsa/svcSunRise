import web
import urllib2, json
import CalcSunRise

urls = ('/SunSetRise', 'SunSetRise')
GeoCodeAPIKey = 'AIzaSyAd3S7rSHOMUbZ964lbTZO_k9zCdrfdJAM'
    
class SunSetRise:
    def GET(self):
        data = web.input()
        geo_address = data.address
        
        maps_location = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + geo_address + '&key=' + GeoCodeAPIKey)
        coordinates = json.load(maps_location)
        maps_location.close
        
        ort_name = ''
        lat = ''
        lng = ''
        
        for location_values in coordinates['results']:
            for loc_items in location_values.iteritems():
                
                    if loc_items[0] == 'formatted_address':
                        ort_name = loc_items[1]
                        
                    if loc_items[0] == 'geometry':
                        for loc_keys in loc_items[1].items():
                            if loc_keys[0] == 'location':
                                lat_lng = loc_keys[1]
                                lat = lat_lng.values()[0]
                                lng = lat_lng.values()[1]
                                
        #print 'ORT: ', ort, 'LAT: ', lat, 'LNG:', lng
        
        SunSetRiseCalcs = CalcSunRise.Ausgabe_Sonnenauf_untergang(lat, lng)
        
        JsonResponse = json.dumps({'ort_info':[{'name':ort_name,'ort_lat':lat,'ort_lng':lng, 'sonnen_auf_untergang':SunSetRiseCalcs}]}, indent=3, sort_keys=True)
        
        web.header('Access-Control-Allow-Origin', 'http://localhost')
        #web.header('Access-Control-Allow-Credentials', 'true')
        return JsonResponse
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
