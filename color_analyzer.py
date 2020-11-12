import numpy as np
import cv2
from copy import deepcopy

'''
image: one-dimensional array which consists of 3-channel(RGB) element
cluster: the number of group to classify

this custom_KMeans clusters color code ignoring true black code(0, 0, 0) 
'''
def custom_KMeans(image_pixels, cluster):
    # Min and Max for RGB
    min_c = 0
    max_c = 255

    # Generate random color points in RGB
    centroids_r = [100, 150, 200]
    centroids_g = [100, 150, 200]
    centroids_b = [100, 150, 200]
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
        num_nonzero_pixels = deepcopy(len(image_pixels))
        # 2. Classify pixels into group
        for i in range(len(image_pixels)):
            distances = np.zeros(cluster)

            # Ignore zero pixels
            if sum(image_pixels[i]) == 0:
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
    labels_ratio = [labels_counter[i]/labels_counter_all for i in range(len(labels_counter))]
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

    centroids_hex = list(zip(centroids_hex, labels_ratio))
    centroids_hex = sorted(centroids_hex, key=lambda x: x[1], reverse=True)

    return centroids_hex

def color_analyzer(original):
    image = cv2.resize(original, dsize=(0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    result = custom_KMeans(image, 3)

    return result

    '''
    k = 3
    clt = KMeans(n_clusters=k)
    clt.fit(image)
    
    rep_colors = []

    i = 0
    for center in clt.cluster_centers_:
        center_ = center.tolist()
        center_hex = []
        for c in center_:
            if int(c) < 16:
                center_hex.append("0" + hex(int(c)))
            else:
                center_hex.append(hex(int(c)))
        center_hex = ''.join(center_hex)
        center_hex = '#' + center_hex.replace("0x", "")
        rep_colors.append({'hex': center_hex, 'ratio': hist[i]})
        i += 1

    hist = centroid_histogram(clt)
    hist = hist.tolist()
    '''

    '''
    bar = plot_colors(hist, clt.cluster_centers_)

    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()
    '''
