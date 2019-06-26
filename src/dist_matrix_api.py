import os, requests, json

def data_read():
    with open(path + "./data/coord_data.txt", "r") as f:
        data = f.readlines()
    data = [[float(v) for v in r.strip().split()] for r in data]
    return data


def key_read():
    with open(path + "./data/API_key.txt", "r") as f:
        data = f.readlines()
    return data[0]


def data_write(dist_matrix):
    with open(path + "./result/distance_matrix.txt", "w") as f:
        for i in dist_matrix:
            for j in i:
                f.write("%.3f\t" % j)
            f.write("\n")


def get_dist_matrix(coord_data):
    size = len(coord_data)
    dist_matrix = [[0 for i in range(size)] for j in range(size)]
    for c1, _ in enumerate(coord_data):
        for c2, _ in enumerate(coord_data):
            if c1!=c2:
                origin = ', '.join(str(e) for e in coordinates[c1])
                destination = ', '.join(str(e) for e in coordinates[c2])
                result = get_drive_time(origin, destination)
                dist_matrix[c1][c2] = result/1000  # meter to km conversion
    return dist_matrix


def get_drive_time(origin, destination):
    url = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}'
           .format(origin.replace(' ','+'),
                   destination.replace(' ','+'),
                   api_key)
            )
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        drive_meter = resp_json_payload['rows'][0]['elements'][0]['distance']['value']
    except:
        print('ERROR: {}, {}'.format(origin, destination))
        drive_meter = 0
    return drive_meter


if __name__ == "__main__":
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    api_key = key_read()
    coordinates = data_read()
    distance_matrix = get_dist_matrix(coordinates)
    data_write(distance_matrix)  # write distance matrix into .txt file
