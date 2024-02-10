import requests


def get_response(coords, map_scale, mode):
    server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": coords,
        "spn": map_scale,
        "l": mode
    }

    response = requests.get(server, params=params)

    if not response:
        return response

    return response


if __name__ == "__main__":
    coords = "30.316526,59.9400798"
    map_scale = "0.6,0.6"
    mode = "map"
    print(get_response(coords, map_scale, mode))
