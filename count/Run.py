import os
from mylib.centroidtracker import CentroidTracker
from mylib.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
from mylib.mailer import Mailer
from mylib import config, thread
import time
import schedule
import csv
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import datetime
from itertools import zip_longest

t0 = time.time()

pwd = os.path.abspath(__file__)
pwd = os.path.dirname(pwd)


def run():
    ret = dict()

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=False, default="mobilenet_ssd/MobileNetSSD_deploy.prototxt",
                    help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=False, default="mobilenet_ssd/MobileNetSSD_deploy.caffemodel",
                    help="path to Caffe pre-trained model")
    ap.add_argument("-i", "--input", required=False, default=pwd+"/videos/example_01.mp4",
                    help="path to video")
    ap.add_argument("-o", "--output", type=str,
                    help="path to optional output video file")
    # confidence default 0.4
    ap.add_argument("-c", "--confidence", type=float, default=0.4,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-s", "--skip-frames", type=int, default=30,
                    help="# of skip frames between detections")
    args = vars(ap.parse_args())

    # initialize the list of class labels MobileNet SSD was trained to
    # detect
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    vs = cv2.VideoCapture(args["input"])

    # initialize the video writer (we'll instantiate later if need be)
    writer = None

    # initialize the frame dimensions (we'll set them as soon as we read
    # the first frame from the video)
    W = None
    H = None

    # instantiate our centroid tracker, then initialize a list to store
    # each of our dlib correlation trackers, followed by a dictionary to
    # map each unique object ID to a TrackableObject
    ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
    trackers = []
    trackableObjects = {}

    # initialize the total number of frames processed thus far, along
    # with the total number of objects that have moved either up or down
    totalFrames = 0
    totalDown = 0
    totalUp = 0
    x = []
    empty = []
    empty1 = []

    # start the frames per second throughput estimator
    fps = FPS().start()

    if config.Thread:
        vs = thread.ThreadingClass(config.url)

    enter_list = []
    exit_list = []
    # loop over frames from the video stream
    while True:
        # grab the next frame and handle if we are reading from either
        # VideoCapture or VideoStream
        frame = vs.read()
        frame = frame[1] if args.get("input", False) else frame

        # if we are viewing a video and we did not grab a frame then we
        # have reached the end of the video
        if args["input"] is not None and frame is None:
            break

        frame = imutils.resize(frame, width=500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # if the frame dimensions are empty, set them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        status = "Waiting"
        rects = []

        if totalFrames % args["skip_frames"] == 0:
            status = "Detecting"
            trackers = []

            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            net.setInput(blob)
            detections = net.forward()

            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    idx = int(detections[0, 0, i, 1])

                    if CLASSES[idx] != "person":
                        continue

                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = box.astype("int")

                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)

                    trackers.append(tracker)
        else:
            # loop over the trackers
            for tracker in trackers:
                # set the status of our system to be 'tracking' rather
                # than 'waiting' or 'detecting'
                status = "Tracking"

                # update the tracker and grab the updated position
                tracker.update(rgb)
                pos = tracker.get_position()

                # unpack the position object
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                # add the bounding box coordinates to the rectangles list
                rects.append((startX, startY, endX, endY))

        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 0), 3)
        cv2.putText(frame, "-Prediction border - Entrance-", (10, H - ((i * 20) + 200)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        objects = ct.update(rects)

        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)

            else:
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

                # check to see if the object has been counted or not
                if not to.counted:
                    if direction < 0 and centroid[1] < H // 2:
                        enter_list.append(objectID)
                        totalUp += 1
                        empty.append(totalUp)
                        to.counted = True

                    elif direction > 0 and centroid[1] > H // 2:
                        exit_list.append(objectID)
                        totalDown += 1
                        empty1.append(totalDown)
                        x = []
                        x.append(len(empty1)-len(empty))
                        if sum(x) >= config.Threshold:
                            cv2.putText(frame, "-ALERT: People limit exceeded-", (10, frame.shape[0] - 80),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
                            if config.ALERT:
                                print("[INFO] Sending email alert..")
                                Mailer().send(config.MAIL)
                                print("[INFO] Alert sent")

                        to.counted = True

            trackableObjects[objectID] = to

            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.circle(
                frame, (centroid[0], centroid[1]), 4, (255, 255, 255), -1)

        ret["enter"] = enter_list
        ret["exit"] = exit_list
        info = [
            ("Exit", totalUp),
            ("Enter", totalDown),
            ("Status", status),
        ]

        info2 = [
            ("Total people inside", x),
        ]

        # Display the output
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        for (i, (k, v)) in enumerate(info2):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (265, H - ((i * 20) + 60)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Initiate a simple log to save data at end of the day
        if config.Log:
            datetimee = [datetime.datetime.now()]
            d = [datetimee, empty1, empty, x]
            export_data = zip_longest(*d, fillvalue='')

            with open('Log.csv', 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(("End Time", "In", "Out", "Total Inside"))
                wr.writerows(export_data)

        # show the output frame
        cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # increment the total number of frames processed thus far and
        # then update the FPS counter
        totalFrames += 1
        fps.update()

        if config.Timer:
            # Automatic timer to stop the live stream. Set to 8 hours (28800s).
            t1 = time.time()
            num_seconds = (t1-t0)
            if num_seconds > 28800:
                break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # close any open windows
    cv2.destroyAllWindows()

    return ret


# learn more about different schedules here: https://pypi.org/project/schedule/
if config.Scheduler:
    # Runs for every 1 second
    # schedule.every(1).seconds.do(run)
    # Runs at every day (9:00 am). You can change it.
    schedule.every().day.at("9:00").do(run)

    while 1:
        schedule.run_pending()

else:
    print(run())
