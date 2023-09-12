# import requests
import sys
import cv2
import numpy as np

# detection algorithms
SIFT  = 'SIFT'
SURF  = 'SURF'
ORB   = 'ORB'
AKAZE = 'AKAZE'
BRISK = 'BRISK'

def circleDetectCropOne(imageName):
    #reading in image
    img = cv2.imread('static/uploads/' + imageName, cv2.IMREAD_COLOR)

    #creating gray scale version of image needed for HoughCircles
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Blurs an image for better edge detection
    #Tested blur, medianBlur, gaussian, and bilateral
    #bilateral produced most accurate outline from test set.
    # imgBlur = cv2.bilateralFilter(gray,9,75,75)

    #original(no blur, minDist, or maxDist)
    # detected_circles = cv2.HoughCircles(imgBlur, cv2.HOUGH_GRADIENT, 0.5, 100, param1=420, param2=10)

    #getting height and width of image
    height = img.shape[0]
    width = img.shape[1]

    #setting max_r so its half the length of the longest direction
    max_r = int(height/2)
    if(height < width):
        max_r = int(width/2)

    #get rid of mini circles
    min_r = int(width/4)
    if(height > width):
        min_r = int(height/4)

    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 0.5, 100, param1= 420, param2=10, minRadius=min_r, maxRadius=max_r)

    #used to detect moon outline
    x, y, radius = (0,0,0)

    #HoughCircles(image, method, dp, minDist, maxDist, param1, param2)
    #cv2.HOUGH_GRADIENT is the only method available at the time is hough circles
    #dp is the inverse ratio of the accumulator resolution to the image resolution.
    #minDist is the minimum distance between the centers of the detected circles
    #maxDist is the maximum distance between the centers of the detected circles
    #parm1 is the higher threshold of the two passed to the Canny edge detector
    #parm2 is the accumulator threshold for the circle centers at the detection stage

    #checks for circles then finds biggest circle with HoughCircle parameters
    if detected_circles is not None:
        detection_circles = np.uint16(np.around(detected_circles))
        for (xc, yc, rc) in detection_circles[0, :]:
            if(rc > radius):
                x = int(xc)
                y = int(yc)
                radius = int(rc)
    else:
        print("circle not detected")

    #original got the first circle from the list and set it to the x,y,r
    # if detected_circles is not None:
    #     detected_circles = np.uint16(np.around(detected_circles))
    #     x, y, radius = int(detected_circles[0][0][0]), int(detected_circles[0][0][1]), int(
    #         detected_circles[0][0][2])
    #     center = (x, y)
    # else:
    #     print("circle not detected")


    ######################### crop image #########################
    #add 15 pixels of padding to get rid of weird cropping of images
    yStart = y - radius - 15
    if (yStart < 0):
        yStart = 0

    yEnd = y + radius + 15
    if (yEnd > height):
        yEnd = height

    xStart = x - radius - 15
    if (xStart < 0):
        xStart = 0

    xEnd = x + radius + 15
    if (xEnd > width):
        xEnd = width

    croppedImg = img[yStart:yEnd, xStart:xEnd]

    # add pixels to the image
    top = y - radius
    if (top >= 0):
        top = 0
    if (top < 0):
        top = - (top)

    bottom = y + radius
    if (bottom <= height):
        bottom = 0
    if (bottom > height):
        bottom = (bottom - height)

    left = x - radius
    if (left >= 0):
        left = 0
    if (left < 0):
        left = -(left)

    right = x + radius
    if (right <= width):
        right = 0
    if (right > width):
        right = right - width

    newImg = cv2.copyMakeBorder(croppedImg, top, bottom, left, right, cv2.BORDER_CONSTANT)
    result = cv2.imwrite(
        'static/processed/resized-' + imageName, newImg)
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")


def circleDetectCropTwo(imageName):
    #reading in image
    img = cv2.imread('static/uploads/' + imageName, cv2.IMREAD_COLOR)

    #creating gray scale version of image needed for HoughCircles
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #getting height and width of image
    height = img.shape[0]
    width = img.shape[1]
    minDimension = min(width, height)

    minR =  int(minDimension / 4)
    maxR = int(minDimension / 3)

    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=minR, maxRadius=maxR)

    #used to detect moon outline
    x, y, radius = (0,0,0)

    #HoughCircles(image, method, dp, minDist, maxDist, param1, param2)
    #cv2.HOUGH_GRADIENT is the only method available at the time is hough circles
    #dp is the inverse ratio of the accumulator resolution to the image resolution.
    #minDist is the minimum distance between the centers of the detected circles
    #maxDist is the maximum distance between the centers of the detected circles
    #parm1 is the higher threshold of the two passed to the Canny edge detector
    #parm2 is the accumulator threshold for the circle centers at the detection stage

    #checks for circles then finds biggest circle with HoughCircle parameters
    if detected_circles is not None:
        detection_circles = np.uint16(np.around(detected_circles))
        for (xc, yc, rc) in detection_circles[0, :]:
            if (rc > radius and xc - rc >= 0 and xc + rc <= width and yc - rc >= 0 and yc + rc <= height):
                x = int(xc)
                y = int(yc)
                radius = int(rc)
    else:
        print("circle not detected")

    # newImg = cv2.copyMakeBorder(croppedImg, top, bottom, left, right, cv2.BORDER_CONSTANT)
    result = cv2.imwrite(
        'static/processed/resized-' + imageName, img[y-radius:y+radius, x-radius:x+radius])
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")


def processUserImage(userImage, modelImage, layerImage, detection):
    #reading in image
    newImg = cv2.imread('static/processed/resized-' + userImage, cv2.IMREAD_COLOR)
    
    ######################### Globe Map #########################
    # Produce a downsampled version of Globe Map
    #Choosing picture from global sample based on the width of the newImage picture
    #Later will be replaced with image from 3D standpoint
    # ppd = round(newImg.shape[1] / 360)
    # if (ppd <= 5):
    #     map = cv2.imread('image-registration/globe_all/05_LRO_ref.jpg')

    # if (ppd <= 7):
    #     map = cv2.imread('image-registration/globe_all/07_LRO_ref.jpg')

    # if (ppd <= 10):
    #     map = cv2.imread('image-registration/globe_all/10_LRO_ref.jpg')

    # if (ppd <= 15):
    #     map = cv2.imread('image-registration/globe_all/15_LRO_ref.jpg')

    # if (ppd <= 20):
    #     map = cv2.imread('image-registration/globe_all/20_LRO_ref.jpg')
    # resize the map
    map = cv2.imread('static/uploads/' + modelImage)
    newMap = cv2.resize(map, (newImg.shape[1], newImg.shape[0]))

    print("H and W for new map", newImg.shape[0], newImg.shape[1])

    print("shape of new map", newMap.shape)

    ######################### Scale-Invariant Feature Transform #########################
    # image regestration features matching (SIFT)

    #cropped image to black and white
    imgG = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)
    # imgGray = cv2.bilateralFilter(imgG,9,75,75)

    #globe image to black and white
    newMapGray = cv2.cvtColor(newMap, cv2.COLOR_BGR2GRAY)
    # newMapGray = cv2.bilateralFilter(newMapG,9,75,75)

    detector = None
    if detection == SIFT:
        detector = cv2.xfeatures2d.SIFT_create()
    elif detection == SURF:
        detector = cv2.xfeatures2d.SURF_create()
    elif detection == ORB:
        detector = cv2.ORB_create(10000)
    elif detection == AKAZE:
        detector = cv2.AKAZE_create()
    elif detection == BRISK:
        detector = cv2.BRISK_create()
    else:
        print(detection, ' does not match supported detection algorithm')
        return None, None
    

    keypoints1, descriptors1 = detector.detectAndCompute(imgG, None)
    keypoints2, descriptors2 = detector.detectAndCompute(newMapGray, None)
    
    #creating BFMatcher
    bf = cv2.BFMatcher()

    #find the keypoints and descriptors with SIFT
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    good_matches = []

    #apply ratio test
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append([m])
    imMatches = cv2.drawMatchesKnn(newImg, keypoints1, newMap, keypoints2, good_matches, None,
                                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # cv2_imshow(imMatches)

    # cv2.waitKey(1)

    result = cv2.imwrite(
        'static/processed/registration-' + detection + "-" + userImage, imMatches)
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")

    # user_to_globe_root = 'processed/globe-' + userImage

    #Warp image section
    # image regestration SIFT
    ref_matched_kpts = np.float32([keypoints1[m[0].queryIdx].pt for m in good_matches])
    sensed_matched_kpts = np.float32([keypoints2[m[0].trainIdx].pt for m in good_matches])

    #Compute homography
    H, status = cv2.findHomography(ref_matched_kpts, sensed_matched_kpts, cv2.RANSAC, 5.0)

    #Warp image
    imgAfterRegistration = cv2.warpPerspective(newImg, H, (newMapGray.shape[0], newMapGray.shape[1]))

    # save processed image
    result = cv2.imwrite(
        'static/processed/transformed-' + detection + "-" + userImage, imgAfterRegistration)
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")

    # stack transformed user image (green) and model image (red)
    r = cv2.cvtColor(imgAfterRegistration, cv2.COLOR_BGR2GRAY)
    g = newMapGray
    b = np.zeros(newMapGray.shape, dtype=np.uint8)
    result = cv2.imwrite(
        'static/processed/stacked-' + detection + "-" + userImage, cv2.merge((b,g,r)))
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")

    r = cv2.cvtColor(imgAfterRegistration, cv2.COLOR_BGR2GRAY)
    g = np.zeros(newMapGray.shape, dtype=np.uint8)
    b = np.zeros(newMapGray.shape, dtype=np.uint8)
    result = cv2.imwrite(
        'static/processed/red-' + detection + "-" + userImage, cv2.merge((b,g,r)))
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")

    r = np.zeros(newMapGray.shape, dtype=np.uint8)
    g = newMapGray
    b = np.zeros(newMapGray.shape, dtype=np.uint8)
    result = cv2.imwrite(
        'static/processed/green-' + detection + "-" + userImage, cv2.merge((b,g,r)))
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")

    # warp layer
    layerImg = cv2.imread('static/uploads/' + layerImage, cv2.IMREAD_COLOR)
    resizedLayerImg = cv2.resize(layerImg, (newImg.shape[1], newImg.shape[0]))
    layerAfterRegistration = cv2.warpPerspective(resizedLayerImg, np.linalg.inv(H), (resizedLayerImg.shape[0], resizedLayerImg.shape[1]))

    ## -- Adding Alpha Channel to User Image --
    # First create the image with alpha channel
    b_channel, g_channel, r_channel = cv2.split(newImg)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.

    rgbaTarget = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    ## -- Making black parts of layer (overlay) image transparent --
    # Convert image to image gray
    tmp = cv2.cvtColor(layerAfterRegistration, cv2.COLOR_BGR2GRAY)
    
    # Applying thresholding technique
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    
    # Using cv2.split() to split channels 
    # of coloured image
    b, g, r = cv2.split(layerAfterRegistration)
    
    # Making list of Red, Green, Blue
    # Channels and alpha
    rgbaOverLay = [b, g, r, alpha]

    transparentLayerImage = cv2.merge(rgbaOverLay, 4)

    ## -- Merge rgba versions of overlay and user images --
    # extract alpha channel from foreground image as mask and make 3 channels
    alpha = transparentLayerImage[:,:,3]
    alpha = cv2.merge([alpha,alpha,alpha])

    # extract bgr channels from foreground image
    front = transparentLayerImage[:,:,0:3]

    result = cv2.imwrite(
        'static/processed/layered-' + detection + "-" + userImage, np.where(alpha==(0,0,0), newImg, front))
    if result == True:
        print("File saved successfully")
    else:
        print("Error in saving file")

    # image_processed_root = 'user_images_processed/processed.jpg'

    # roots= [image_processed_root , user_to_globe_root]
    # # some code here to process the WAC to be able to be used later in our 3D model
    # # what needs to be processed is to cut it in the edges
    # # once is cut and processed save the image in the folder static/WAC_resized/
    # # map_resize()

    # return roots

if __name__ == "__main__":
    circleDetectCropOne(sys.argv[1])
    for d in [SURF, SIFT, ORB, AKAZE, BRISK]:
        processUserImage(sys.argv[1], sys.argv[2], sys.argv[3], d)
