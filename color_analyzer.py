import numpy as np
import cv2
from copy import deepcopy
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from sklearn.cluster import KMeans

'''
image: one-dimensional array which consists of 3-channel element
cluster: the number of group to classify

this custom_KMeans clusters color code ignoring true black code(0, 0, 0) 
'''
def custom_KMeans(image_pixels, cluster):
    # Min and Max for RGB
    min_c = 0
    max_c = 255

    # Generate random color points in RGB
    #centroids_r = np.random.uniform(min_c, max_c, cluster)
    #centroids_g = np.random.uniform(min_c, max_c, cluster)
    #centroids_b = np.random.uniform(min_c, max_c, cluster)
    centroids_r = [64, 128, 172]
    centroids_g = [64, 128, 172]
    centroids_b = [64, 128, 172]
    centroids = np.array(list(zip(centroids_r, centroids_g, centroids_b)))

    def euclidean_distance(center, target):
        return (center[0] - target[0]) ** 2 + \
               (center[1] - target[1]) ** 2 + \
               (center[2] - target[2]) ** 2

    centroids_old = np.zeros(centroids.shape)
    labels_for_pixels = np.full(len(image_pixels), cluster)
    labels_counter = np.zeros(cluster)
    error = np.zeros(cluster)

    # Initialize error
    for i in range(cluster):
        error[i] = euclidean_distance(centroids_old[i], centroids[i])

    # 4. Iterate while error converges to 0
    while error.all() != 0:
        # 2. Classify pixels into group
        for i in range(len(image_pixels)):
            distances = np.zeros(cluster)

            # Ignore zero pixels
            if sum(image_pixels[i]) <= 50:
                continue

            # calculate euclidean distance to find out appropriate color group
            for j in range(cluster):
                distances[j] = euclidean_distance(centroids[j], image_pixels[i])

            cluster_idx = np.argmin(distances)
            labels_for_pixels[i] = cluster_idx
            labels_counter[cluster_idx] += 1

        # 3. Update centroids for better clustering
        centroids_old = deepcopy(centroids)
        for i in range(cluster):
            # Collecting ith label members
            members = [image_pixels[j] for j in range(len(image_pixels))
                       if labels_for_pixels[j] == i and sum(image_pixels[j]) != 0]
            # Select new centroids
            centroids[i] = np.mean(members, axis=0)

        # Recalculate error
        for i in range(cluster):
            error[i] = euclidean_distance(centroids_old[i], centroids[i])

    labels_counter_all = sum(labels_counter)
    labels_ratio = [labels_counter[i]/labels_counter_all for i in range(cluster)]
    centroids_hex = []
    for center in centroids:
        center_hex = []
        for code in center:
            if int(code) < 16:
                center_hex.append("0" + hex(int(code)))
            else:
                center_hex.append(hex(int(code)))
        center_hex = ''.join(center_hex)
        center_hex = '#' + center_hex.replace("0x", "")
        centroids_hex.append(center_hex)

    centroids_result = []
    for i in range(cluster):
        centroids_result.append({'hex': centroids_hex[i], 'ratio': labels_ratio[i]})
    centroids_result = sorted(centroids_result, key=lambda x: x['ratio'], reverse=True)

    return centroids_result


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=num_labels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def color_analyzer(original):
    image = cv2.resize(original, dsize=(0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)

    # Reshape to one-dimensional RGB array adapting alpha channel
    lab_onedim = []
    for r in image:
        for c in r:
            if c[3] >= 200:
                rgb = sRGBColor(c[2], c[1], c[0], is_upscaled=True)
                lab = convert_color(rgb, LabColor, through_rgb_type=sRGBColor)
                lab_onedim.append([lab.lab_l, lab.lab_a, lab.lab_b])

    # start K-Means Clustering
    clt = KMeans(n_clusters=3)
    clt.fit(lab_onedim)

    hist = centroid_histogram(clt)
    hist = hist.tolist()

    result = []
    i = 0
    for center in clt.cluster_centers_:
        lab = LabColor(center[0], center[1], center[2])
        rgb = convert_color(lab, sRGBColor, through_rgb_type=sRGBColor)
        rgb = [int(rgb.rgb_r * 255), int(rgb.rgb_g * 255), int(rgb.rgb_b * 255)]

        center_hex = []
        for c in rgb:
            if int(c) < 16:
                center_hex.append("0" + hex(int(c)))
            else:
                center_hex.append(hex(int(c)))
        center_hex = '#' + ''.join(center_hex).replace("0x", "")
        result.append({'hex': center_hex, 'lab': center.tolist(), 'ratio': hist[i]})
        i += 1

    result = sorted(result, key=lambda x: x['ratio'], reverse=True)
    return result
