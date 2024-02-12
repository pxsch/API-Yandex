import requests


def get_response(coords, map_scale, mode, point_coords):
    server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": coords,
        "spn": map_scale,
        "l": mode,
        "size": "650,400"
    }

    if point_coords:
        params["pt"] = f"{point_coords},pm2lbm"

    response = requests.get(server, params=params)

    if not response:
        return False, response

    return True, response


def geocoder_request(user_request):
    request = "https://geocode-maps.yandex.ru/1.x/" \
              "?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
              f"&geocode={user_request}&format=json"

    response = requests.get(request)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return True, toponym_coodrinates

    return False, response


if __name__ == "__main__":
    coords = "30.316526,59.9400798"
    map_scale = "0.6,0.6"
    mode = "map"
    print(get_response(coords, map_scale, mode))
    print(geocoder_request(input()))
