import math

class Tracker:
    def __init__(self):
        self.center_points = {}
        self.id_count = 0
        self.max_lost_frames = 5  # Maximum number of frames without detection

    def update(self, objects_rect):
        objects_bbs_ids = []
        active_ids = []

        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + w) // 2
            cy = (y + h) // 2

            closest_object_id = None
            min_distance = float('inf')

            for object_id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < min_distance:
                    closest_object_id = object_id
                    min_distance = dist

            if closest_object_id is not None and min_distance < 35:
                self.center_points[closest_object_id] = (cx, cy, 0)
                objects_bbs_ids.append([x, y, w, h, closest_object_id])
                active_ids.append(closest_object_id)
            else:
                self.center_points[self.id_count] = (cx, cy, 1)  # Fix 1: Initialize lost frames counter to 1
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        objects_to_delete = []
        for object_id in self.center_points.keys():
            if object_id not in active_ids:
                if self.center_points[object_id][2] >= self.max_lost_frames:
                    objects_to_delete.append(object_id)
                else:
                    self.center_points[object_id] = (
                        self.center_points[object_id][0],
                        self.center_points[object_id][1],
                        self.center_points[object_id][2] + 1
                    )

        for object_id in objects_to_delete:
            del self.center_points[object_id]  # Fix 3: Delete objects after iterating

        return objects_bbs_ids
