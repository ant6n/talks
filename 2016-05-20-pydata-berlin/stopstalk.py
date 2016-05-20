
import json

def packStopsJson(stops):
    stopsArray = [
        {
            'name': stop['name'],
            'lat':  stop['lat'],
            'lng':  stop['lng'],
            'code': stop['code'],
            'isStation': stop['isStation'],
            'servicePatternId': stop['servicePatternId']
        }
        for stop in stops]
    return json.dumps(stopsArray, indent=2)


#import msgpack
def packStopsMsgpack(stops):
    stopsArray = [
        {
            'name': stop['name'],
            'lat':  stop['lat'],
            'lng':  stop['lng'],
            'code': stop['code'],
            'isStation': stop['isStation'],
            'servicePatternId': stop['servicePatternId']
        }
        for stop in stops]
    return msgpack.packb(stopsArray)


#import msgpack
from io import BytesIO

def msgpackStop(stop, buf):    
    stopCode = int(stop['code'] or 0)
    buf.write(msgpack.packb(stop['name']))
    buf.write(msgpack.packb(stop['lat']))
    buf.write(msgpack.packb(stop['lng']))
    buf.write(msgpack.packb(stopCode))
    buf.write(msgpack.packb(stop['isStation']))
    buf.write(msgpack.packb(stop['servicePatternId']))
    
    
def msgpackStops(stops, buf):
    buf.write(msgpack.packb(len(stops)))
    for stop in stops:
        msgpackStop(stop, buf)


def msgpackStopsString(stops):
    buf = BytesIO()
    msgpackStops(stops, buf)
    buf.seek(0)    
    return buf.read()




#import capnp
#import stops_capnp
def protoPackStop(stop):
    stopCode = int(stop['code'] or 0)
    stop = stops_capnp.Stop.new_message(
        name = stop['name'].encode('utf-8'),
        lat = stop['lat'],
        lng = stop['lng'],
        code = stopCode,
        isStation = stop['isStation'],
        servicePatternId = stop['servicePatternId'],
    )
    return stop

def protoPackStops(stops):
    stopObjects = [protoPackStop(stop) for stop in stops]
    result = stops_capnp.Stops.new_message(stops = stopObjects)
    return result

def writeStops(stops, f):
    f.write(protoPackStops(stops))


def proto():
    f = open("vbb-stops")
    stops = json.loads(f.read())
    protoStops = protoPackStops(stops)
    
    f = open("proto-stop", "wb")
    protoStops.write(f)
    f.close()
    
    stopData = open("proto-stop").read()



import namedstruct

def packStop(stop):
    # convert lat/lng to int
    intLat = int(round(stop['lat']*1e7))
    intLng = int(round(stop['lng']*1e7))

    # create stop struct
    stopObject = (
        namedstruct.Struct("Stop")
        .addString('name', stop['name'], referenceBitWidth=8)
        .addUInt8 ('isStation', stop['isStation'])
        .addInt32 ('lat', intLat)
        .addInt32 ('lng', intLng)
        .addUInt32('code', int(stop['code'] or 0))
        .addUInt32('servicePatternId', stop['servicePatternId'])
    )
    return stopObject

def packStops(stops):
    stopObjects = [packStop(stop) for stop in stops]
    stopsObject = namedstruct.Struct("Stops")
    stopsObject.addArray("stops", stopObjects)
    return stopsObject




def packStop2(stop):
    # convert lat/lng to int
    intLat = int(round(stop['lat']*1e7))
    intLng = int(round(stop['lng']*1e7))

    # create stop struct
    stopObject = (
        namedstruct.Struct("Stop")
        .addString('name', stop['name'], referenceBitWidth=8)
        .addUInt8 ('isStation', stop['isStation'])
        .addInt32 ('lat', intLat)
        .addInt32 ('lng', intLng)
        .addUInt32('code', int(stop['code'] or 0))
        .addUInt32('servicePatternId', stop['servicePatternId'])
    )
    return stopObject

def packStops2(stops):
    stopObjects = [packStop(stop) for stop in stops]
    stopsObject = namedstruct.Struct("Stops")
    stopsObject.addArray("stops", stopObjects)
    return stopsObject

