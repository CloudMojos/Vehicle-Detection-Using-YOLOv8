from typing import Tuple

from ultralytics import YOLO
import cv2
import math
import numpy as np
from datetime import datetime, timedelta
import time
# Part of new detection
from deep_sort_realtime.deepsort_tracker import DeepSort
# Part of newer detection
from deep_sort.deep_sort.tracker import Tracker
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection
from deep_sort.tools import generate_detections as gdet
from db_connection import insert_traffic_data

from collections import deque

# Part of new detection
# CONFIDENCE_THRESHOLD = 0.8
# Part of newer detection
conf_threshold = 0.5
max_cosine_distance = 0.4
nn_budget = None

end_point1 = (0, 0)
end_point2 = (0, 0)

counter_end: int = 0

date = ''
time_start = ''
address = ''

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

points = [deque(maxlen=32) for _ in range(1000)]  # list of dequeues to store the points
counted_ids = set()  # Set to store counted track IDs

# Part of newer detection
model_filename = "config/mars-small128.pb"
encoder = gdet.create_box_encoder(model_filename, batch_size=1)
metric = nn_matching.NearestNeighborDistanceMetric(
    "cosine", max_cosine_distance, nn_budget)
tracker = Tracker(metric)
# load the class labels the YOLO model was trained on
# classes_path = "config/coco.names"
# # classes_path = "config/new.txt"
# with open(classes_path, "r") as f:
#     class_names = f.read().strip().split("\n")
class_names = ['Bicycle', 'Bus', 'Car', 'Jeepney', 'Motorcycle', 'Tricycle', 'Truck', '-']
# create a list of random colors to represent each class

np.random.seed(42)  # to get the same colors
colors = np.random.randint(0, 255, size=(len(class_names), 3))  # (80, 3)


def create_video_writer(video_cap, output_filename):
    # grab the width, height, and fps of the frames in the video stream.
    frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_cap.get(cv2.CAP_PROP_FPS))

    # initialize the FourCC and a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_filename, fourcc, fps,
                             (frame_width, frame_height))

    return writer


def update_lines(s1, s2, e1, e2):
    global end_point1, end_point2

    end_point1 = e1
    end_point2 = e2

    print("Updated line: ")
    print(e1, e2)
    return


def update_datetime(d, t):
    global date, time_start

    date = str(d)
    time_start = str(t)
    print(date)
    print(time_start)
    return


def update_address(a):
    global address

    address = str(a)
    return


def video_detection(path_x):
    global counter_end

    global end_point1
    global end_point2

    global metric
    global tracker

    global date
    global time_start
    global address
    video_capture = path_x
    # Create a Webcam Object
    cap = cv2.VideoCapture(video_capture)
    if (path_x == 0):
        cap.open("http://192.168.0.82:8080/video")
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
    out = create_video_writer(cap, "output.mp4")


    model = YOLO("../weights/yes.pt")
    # Commented out. Part of New Detection Code
    # tracker = DeepSort(max_age=50)


    # class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    # "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    # "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    # "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    # "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    # "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
    # "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
    # "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    # "teddy bear", "hair drier", "toothbrush" ]
    while True:
        start = datetime.now()

        success, img = cap.read()
        # if there is no frame, we have reached the end of the video
        if not success:
            print("End of the video file...")
            break

        overlay = img.copy()
        # draw the lines
        cv2.line(img, end_point1, end_point2, (0, 255, 0), 12)

        img = cv2.addWeighted(overlay, 0.5, img, 0.5, 0)
        # *************************************** #
        # *    Old code for object detection    * #
        # *************************************** #
        results = model(img, stream=True)
        #
        # for r in results:
        #     boxes = r.boxes
        #     for box in boxes:
        #         cls = int(box.cls[0])
        #         if 1 < cls < 7:
        #             x1, y1, x2, y2 = box.xyxy[0]
        #             x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        #             class_name = class_names[cls]
        #             conf = math.ceil((box.conf[0] * 100)) / 100
        #             label = f'{class_name}{conf}'
        #             t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
        #             print(t_size)
        #             c2 = x1 + t_size[0], y1 - t_size[1] - 3
        #             cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
        #             cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        #             cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        # # *************************************** #
        # # *    New code for object detection    * #
        # # *************************************** #
        #
        # # run the YOLO model on the frame
        # detections = model(img)[0]
        #
        # # initialize the list of bounding boxes and confidences
        # results = []
        #
        # # loop over the detections
        # for data in detections.boxes.data.tolist():
        #     # extract the confidence (i.e., probability) associated with the prediction
        #     confidence = data[4]
        #
        #     # filter out weak detections by ensuring the
        #     # confidence is greater than the minimum confidence
        #     if float(confidence) < CONFIDENCE_THRESHOLD:
        #         continue
        #
        #     # if the confidence is greater than the minimum confidence,
        #     # get the bounding box and the class id
        #     xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        #     class_id = int(data[5])
        #     # add the bounding box (x, y, w, h), confidence and class id to the results list
        #     results.append([[xmin, ymin, xmax - xmin, ymax - ymin], confidence, class_id])
        #
        # # *************************************** #
        # # *               TRACKING              * #
        # # *************************************** #
        # # update the tracker with the new detections
        # tracks = tracker.update_tracks(results, frame=img)
        # # loop over the tracks
        # for track in tracks:
        #     # if the track is not confirmed, ignore it
        #     if not track.is_confirmed():
        #         continue
        #
        #     # get the track id and the bounding box
        #     track_id = track.track_id
        #     ltrb = track.to_ltrb()
        #
        #     xmin, ymin, xmax, ymax = int(ltrb[0]), int(
        #         ltrb[1]), int(ltrb[2]), int(ltrb[3])
        #     # draw the bounding box and the track id
        #     cv2.rectangle(img, (xmin, ymin), (xmax, ymax), GREEN, 2)
        #     cv2.rectangle(img, (xmin, ymin - 20), (xmin + 20, ymin), GREEN, -1)
        #     cv2.putText(img, str(track_id), (xmin + 5, ymin - 8),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)

        # *************************************** #
        # *   Newer code for object detection   * #
        # *************************************** #
        for result in results:
            # initialize the list of bounding boxes, confidences, and class IDs
            bboxes = []
            confidences = []
            class_ids = []
            # loop over the detections
            for data in result.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = data
                x = int(x1)
                y = int(y1)
                w = int(x2) - int(x1)
                h = int(y2) - int(y1)
                class_id = int(class_id)
                # filter out weak predictions by ensuring the confidence is
                # greater than the minimum confidence
                if confidence > conf_threshold:
                    bboxes.append([x, y, w, h])
                    confidences.append(confidence)
                    class_ids.append(class_id)
                    # # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # # *************************************** #
            # # *               TRACKING              * #
            # # *************************************** #
            # get the names of the detected objects
            names = [class_names[class_id] for class_id in class_ids]
            # get the features of the detected objects
            features = encoder(img, bboxes)
            # convert the detections to deep sort format
            dets = []
            for bbox, conf, class_name, feature in zip(bboxes, confidences, names, features):
                dets.append(Detection(bbox, conf, class_name, feature))
            # run the tracker on the detections
            tracker.predict()
            tracker.update(dets)

            # loop over the tracked objects
            for track in tracker.tracks:
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue
                # get the bounding box of the object, the name
                # of the object, and the track id
                bbox = track.to_tlbr()
                track_id = track.track_id
                class_name = track.get_class()
                # conf = round(track.covariance, 2)
                # convert the bounding box to integers
                x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                # get the color associated with the class name
                class_id = class_names.index(class_name)
                color = colors[class_id]
                B, G, R = int(color[0]), int(color[1]), int(color[2])
                # draw the bounding box of the object, the name
                # of the predicted object, and the track id
                text = str(track_id) + " - " + class_name + " "
                cv2.rectangle(img, (x1, y1), (x2, y2), (B, G, R), 3)
                cv2.rectangle(img, (x1 - 1, y1 - 20),
                              (x1 + len(text) * 12, y1), (B, G, R), -1)
                cv2.putText(img, text, (x1 + 5, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                ############################################################
                ### Count the number of vehicles passing the lines       ###
                ############################################################
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                # append the center point of the current object to the points list
                points[track_id].append((center_x, center_y))
                cv2.circle(img, (center_x, center_y), 4, (0, 255, 0), -1)
                # loop over the set of tracked points and draw them
                for i in range(1, len(points[track_id])):
                    point1 = points[track_id][i - 1]
                    point2 = points[track_id][i]
                    # if the previous point or the current point is None, do nothing
                    if point1 is None or point2 is None:
                        continue
                    cv2.line(img, point1, point2, (0, 255, 0), 2)

                # get the last point from the points list and draw it
                last_point_x = points[track_id][0][0]
                last_point_y = points[track_id][0][1]
                cv2.circle(img, (int(last_point_x), int(last_point_y)), 4, (255, 0, 255), -1)
                # if the y coordinate of the center point is below the line, and the x coordinate is
                # between the start and end points of the line, and the last point is above the line,
                # # increment the total number of cars crossing the line and remove the center points from the list
                if track_id not in counted_ids:
                    if (end_point1[0] <= center_x <= end_point2[0] or end_point2[0] <= center_x <= end_point1[0]) and \
                            (end_point1[1] <= center_y <= end_point2[1] or end_point2[1] <= center_y <= end_point1[1]):
                        counter_end += 1

                        time_since_start = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                        total_time = add_time(time_start, time_since_start)
                        time_out = total_time
                        time_in = time_out
                        text = f"Track ID: {track_id}, Class Name: {class_name}, Start Time: {time_in}, End Time: {time_out}"
                        print(text)
                        counted_ids.add(track_id)
                        success_id = insert_traffic_data(class_name, date, time_in, time_out, address)
                        print("Success ID inserted: ", success_id)
                        points[track_id].clear()
        # *************************************** #
        # *           POST PROCESSING           * #
        # *************************************** #

        # end time to compute the fps
        end = datetime.now()
        # calculate the frame per second and draw it on the frame
        fps = f"FPS: {1 / (end - start).total_seconds():.2f}"
        cv2.putText(img, fps, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 8)

        endx = int((end_point1[0] + end_point2[0]) / 2)
        endy = int((end_point1[1] + end_point2[1]) / 2)

        # draw the total number of vehicles passing the lines
        cv2.putText(img, "A", (end_point1[0], endy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, f"{counter_end}", (endx, endy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img, f"{counter_C}", (1040, 483), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        yield img
        out.write(img)
        # cv2.imshow("image", img)
        # if cv2.waitKey(1) & 0xFF==ord('1'):
        #     break

    counter_end = 0

    tracker = Tracker(metric)
    out.release()


def get_one_frame(path_x):
    # Open the video file
    cap = cv2.VideoCapture(path_x)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return None

    while True:
        ret, frame = cap.read()

        if ret:
            cap.release()
            return frame


def add_time(t: str, seconds_to_add: float) -> str:
    """
    Adds seconds to a given time in hh:mm format.
    Args:
        time (str): Time in hh:mm format.
        seconds_to_add (float): Seconds to add.
    Returns:
        str: New time in hh:mm:ss format.
    """
    # Parse the input time
    hours, minutes = map(int, t.split(':'))

    # Calculate the total seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds_to_add

    # Calculate new hours, minutes, and seconds
    new_hours, remainder = divmod(total_seconds, 3600)
    new_minutes, new_seconds = divmod(remainder, 60)

    new_hours = int(new_hours)
    new_minutes = int(new_minutes)
    new_seconds = float(new_seconds)

    # Convert seconds to integer part and decimal part
    seconds_integer = int(new_seconds)
    seconds_decimal = int((new_seconds - seconds_integer) * 100)  # Extract two decimal places
    # Format the result
    new_time = f"{new_hours:02d}:{new_minutes:02d}:{seconds_integer:02d}.{seconds_decimal:02d}"
    return new_time

# # Example usage:
# time_input = "12:47"
# seconds_to_add_input = 3660.23
# new_time_result = add_time(time_input, seconds_to_add_input)
# print(f"New time: {new_time_result}")


cv2.destroyAllWindows()