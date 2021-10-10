from collections import namedtuple
from math import sqrt
import random
import ImageFilter
import psycopg2
from psycopg2 import OperationalError

try:
    import Image
except ImportError:
    from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))
rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))
white = 0
black = 0
geom = 0


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def get_image(img_url):
    img = Image.open(img_url)
    h, w = img.size
    h = int(h)
    w = int(w)
    image = img.crop((0, 0, w / 1.6, h / 1.6))
    half = crop_max_square(image)
    return image


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def colorz(img, n=3):
    img.thumbnail((200, 200))
    w, h = img.size
    points = get_points(img)
    clusters = kmeans(points, n, 1)
    return clusters


def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))


def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))
        print(diff)
        if diff < min_diff:
            break

    return clusters


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            options="-c search_path=dbo,networkstreetlighting"
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    print(connection.get_dsn_parameters())
    return connection


def processing_database(geo, brightness):
    connection = create_connection('test', "postgres", '1',
                                   'localhost', '4523')
    con = connection.cursor()
    con.execute(f"INSERT INTO lights (longitude, latitude, brightness) VALUES ({geo}, {brightness})")
    connection.commit()
    con.close()
    connection.close()


def main(white=0, black=0, img_url='', img_id=0, geo=0):
    image = get_image(img_url)

    clusters = get_points(image)
    for p in clusters:
        r = p[0][0]
        g = p[0][1]
        b = p[0][2]
        if (255 >= r >= 120) and (255 >= g >= 120) and (255 >= b >= 120):
            white += 1
        if (119 >= r >= 0) and (119 >= g >= 0) and (119 >= b >= 0):
            black += 1
    percent = int(white / (black + white) * 100)
    print(img_id, percent, geo)
    processing_database(geo, percent)
    return percent
