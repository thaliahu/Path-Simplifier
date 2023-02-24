"""Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: Thalia Hundt
Credits: TBD
"""

import csv
import doctest

import geometry
import map_view
import config


def read_points(path: str) -> list[tuple[float, float]]:
    xy_list = []
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            xy_list.append((float(row[0]), float(row[1])))
    return(xy_list)


def summarize(points: list[tuple[float, float]],
              tolerance: int = config.TOLERANCE_METERS,
              ) -> list[tuple[float, float]]:
    summary: list[tuple[float, float]] = [points[0]]
    epsilon = float(tolerance * tolerance)

    def simplify(start: int, end: int):
        """Add necessary points in (start, end] to summary."""

        outliers = []
        maxdist = 0.0
        maxidx = 0
        for i in range(start, end):
            dist = geometry.deviation_sq(points[start], points[end],
                                         points[i])
            if dist > epsilon:
                outliers.append(i)
                if dist > maxdist:
                    maxdist = dist
                    maxidx = i

        # Base case - simply add end point.
        if len(outliers) == 0:
            summary.append(points[end])
            return

        # Recursive case - two calls to simplify
        simplify(start, maxidx)
        simplify(maxidx, end)
        return

    # Start search between first and last point in the list.
    simplify(0, len(points)-1)
    return summary


def main():
    points = read_points(config.UTM_CSV)

    # Quick check for correctness.
    path = [(0,0), (1,1), (2,2), (2,3), (2,4), (3,4), (4,4)]
    expect = [(0,0), (2,2), (2,4), (4,4)]
    simple = summarize(path, tolerance=0.5)
    if simple != expect:
        raise AssertionError('incorrect result')

    # Main problem.
    summary = summarize(points, config.TOLERANCE_METERS)    
    map_view.init()
    for point in summary:
        map_view.plot_to(point)
    map_view.clean_scratches()
    map_view.wait_to_close()


if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()
