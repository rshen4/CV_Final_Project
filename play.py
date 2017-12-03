#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np
from body_coord import body_coord, position_3D, plot_vector
# some change
#kmnfwkonfhjjh

cv2.namedWindow('Depth')


def main():
    keep_running = True


    while keep_running:
        depth_frame = np.array(get_depth())
        color_frame = np.array(get_video())
        #only works to about 90

        hand_position = find_min_idx(depth_frame)
        hand_depth = depth_frame[hand_position[0], hand_position[1]]

        #radius_hand = 50
        #cv2.circle(depth_frame, closest, radius_hand, (0,255,0), 4)
        #im2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        #depth_image_dist = cv2.distanceTransform(threshold, cv2.DIST_L2, 5)

        body_frame = body_coord(depth_frame)

        #radius_body = 10
        #cv2.circle(depth_frame, (body_coord_row, body_coord_col), radius_body, (255,0,0),4)
        #cv2.imshow('Depth', depth_frame)

        hand_position_3D = position_3D(hand_position, hand_depth, body_frame)
        # make this a ros topic for baxter to receive, scale z (depth) into a suitable value, current scale is 500
        print hand_position_3D

        color_frame_vector = plot_vector(color_frame, hand_position, body_frame)
        cv2.imshow('body frame', color_frame_vector)

        if cv2.waitKey(10) == 27:
            keep_running = False


def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])

def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

def find_min_idx(x):
    k = x.argmin()
    ncol = x.shape[1]
    return (k%ncol, k/ncol)


if __name__ == "__main__":
    main()