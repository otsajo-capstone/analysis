from palette import *


def lab_euclidean_distance(center, p_color):
    return (center[0] - p_color[0]) ** 2 + \
           (center[1] - p_color[1]) ** 2 + \
           (center[2] - p_color[2]) ** 2


def p_color_classifier(centroids_result):
    result = []
    colors = []

    for centroid in centroids_result:
        lab = centroid['lab']
        ratio = centroid['ratio']

        min_dist = 16777216
        p_color_type = ''
        p_color_subtype = ''

        # spring
        for c in spring_warm_labeled_LAB:
            temp_dist = lab_euclidean_distance(lab, c['lab'])
            if min_dist > temp_dist:
                min_dist = temp_dist
                p_color_subtype = c['subtype']
                p_color_type = '봄 웜'

        # summer
        for c in summer_cool_labeled_LAB:
            temp_dist = lab_euclidean_distance(lab, c['lab'])
            if min_dist > temp_dist:
                min_dist = temp_dist
                p_color_subtype = c['subtype']
                p_color_type = '여름 쿨'

        # autumn
        for c in autumn_warm_labeled_LAB:
            temp_dist = lab_euclidean_distance(lab, c['lab'])
            if min_dist > temp_dist:
                min_dist = temp_dist
                p_color_subtype = c['subtype']
                p_color_type = '가을 웜'

        # winter
        for c in winter_cool_labeled_LAB:
            temp_dist = lab_euclidean_distance(lab, c['lab'])
            if min_dist > temp_dist:
                min_dist = temp_dist
                p_color_subtype = c['subtype']
                p_color_type = '겨울 쿨'

        duplicate_flag = 0
        i = 0
        for r in result:
            if r['type'] == p_color_type:
                duplicate_flag = 1
                new_ratio = r['ratio'] + ratio
                result[i]['ratio'] = new_ratio
                break
            i += 1

        if duplicate_flag == 0:
            result.append({
                "ratio": ratio,
                "type": p_color_type,
            })

        colors.append({
            "hex": centroid['hex'],
            "ratio": ratio,
            "type": p_color_type,
            "subtype": p_color_subtype
        })

    result = sorted(result, key=lambda x: x['ratio'], reverse=True)

    return result, colors

