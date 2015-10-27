import web
import urllib2, json
import time

urls = ('/SunSetRise', 'SunSetRise')
GeoCodeAPIKey = 'AIzaSyAd3S7rSHOMUbZ964lbTZO_k9zCdrfdJAM'
    
class SunSetRise:
    def GET(self):
        data = web.input()
        geo_address = data.address
        
        calc_date = data.date
        
        maps_location = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + geo_address + '&key=' + GeoCodeAPIKey)
        coordinates = json.load(maps_location)
        maps_location.close
        
        ort_name = ''
        lat = ''
        lng = ''
        
        # Filter coordinates for location
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
        
        
        if calc_date == "":
            calc_date = time.strftime("%Y-%m-%d")
        
        # get SunSetRise data from web service and load JSON    
        getSunSetRise = urllib2.urlopen('http://api.geonames.org/timezoneJSON?lat=' + str(lat) + '&lng=' + str(lng) + '&date='+ calc_date + '&username=nnikolic')
        SunSetRise = json.load(getSunSetRise)
        
        actual_timezoneId = SunSetRise['timezoneId']
        
        for actual_date in SunSetRise['dates']:
            
            a_sunrise = actual_date['sunrise']
            a_sunset = actual_date['sunset']
        
        # Create JSON Object
        JsonResponse = json.dumps({'name':ort_name,'ort_lat':lat,'ort_lng':lng,'timezone':actual_timezoneId, 'sonnen_aufgang':a_sunrise, 'sonnen_untergang':a_sunset}, indent=3, sort_keys=True)
        
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        
        print JsonResponse
        
        return JsonResponse
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
