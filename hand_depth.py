import freenect
import cv2
import frame_convert2
import numpy as np
import  time

keep_running = True


def main():


    while keep_running:
        depth_image = np.array(get_depth())
        color_image = np.array(get_video())
        closest = find_min_idx(depth_image)

        [x, y] = closest
        z = depth_image[x][y]
        depth_thresh = 20
        hand = np.where(np.logical_and(depth_image<= (z+depth_thresh), depth_image>=z))
        #print hand
        size_thresh = 8000
        #x1, y1 = hand.shape
        num = hand[0]
        num = num.size
        print num
        if num > size_thresh:
            s = 'ONE'
        else:
            s = 'ZERO'

       	print s
        #color_image[100:400, 50:300] = image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(depth_image, s, (100, 450), font, 2, (255, 10, 10), 2, cv2.LINE_AA)
        cv2.imshow('Depth_Image', depth_image)
        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()

    return s




def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

def find_min_idx(x):
    k = x.argmin()
    ncol = x.shape[1]
    return k/ncol, k%ncol


if __name__ == "__main__":
    main()