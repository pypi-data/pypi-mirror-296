from cooptools.geometry_utils import vector_utils as vec

def do_convex_polygons_intersect(poly_a: vec.IterVec, poly_b: vec.IterVec):
    for polygon in [poly_a, poly_b]:
        for i1 in range(len(poly_a)):
            i2 = (i1 + 1) % len(polygon)
            p1 = polygon[i1]
            p2 = polygon[i2]

            normal = (p2[1] - p1[1], p1[0] - p2[0])

            minA, maxA = None, None

            for p in poly_a:
                projected = normal[0] * p[0] + normal[1] * p[1]
                if (minA is None or projected < minA):
                    minA = projected
                if (maxA is None or projected > maxA):
                    maxA = projected


            minB, maxB = None, None

            for p in poly_b:
                projected = normal[0] * p[0] + normal[1] * p[1]
                if (minB is None or projected < minB):
                    minB = projected
                if (maxB is None or projected > maxB):
                    maxB = projected

            if (maxA < minB or maxB < minA):
                return False

    return True


if __name__ == "__main__":
    def test01():
        ret = do_convex_polygons_intersect(
            [(0, 0), (0, 100), (100, 100), (100, 0)],
            [(50, 0), (50, 100), (150, 100), (150, 0)]
        )
        assert ret == True

    def test02():
        ret = do_convex_polygons_intersect(
            [(0, 0), (0, 100), (100, 100), (100, 0)],
            [(250, 0), (250, 100), (350, 100), (350, 0)]
        )
        assert ret == False

    test01()
    test02()
