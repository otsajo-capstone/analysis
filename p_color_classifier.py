from palette import *

def range_generator(str):
    big_num = str[0]
    rest_num = str[1:]
    range = []

    if big_num == '0':
        range.append('000000')
        range.append('4' + rest_num)
    elif big_num == '1':
        range.append('000000')
        range.append('4' + rest_num)
    elif big_num == '2':
        range.append('0' + rest_num)
        range.append('4' + rest_num)
    elif big_num == '3':
        range.append('1' + rest_num)
        range.append('5' + rest_num)
    elif big_num == '4':
        range.append('2' + rest_num)
        range.append('6' + rest_num)
    elif big_num == '5':
        range.append('3' + rest_num)
        range.append('7' + rest_num)
    elif big_num == '6':
        range.append('4' + rest_num)
        range.append('8' + rest_num)
    elif big_num == '7':
        range.append('5' + rest_num)
        range.append('9' + rest_num)
    elif big_num == '8':
        range.append('6' + rest_num)
        range.append('a' + rest_num)
    elif big_num == '9':
        range.append('7' + rest_num)
        range.append('b' + rest_num)
    elif big_num == 'a' or big_num == 'A':
        range.append('8' + rest_num)
        range.append('c' + rest_num)
    elif big_num == 'b' or big_num == 'B':
        range.append('9' + rest_num)
        range.append('d' + rest_num)
    elif big_num == 'c' or big_num == 'C':
        range.append('a' + rest_num)
        range.append('e' + rest_num)
    elif big_num == 'd' or big_num == 'D':
        range.append('b' + rest_num)
        range.append('f' + rest_num)
    elif big_num == 'e' or big_num == 'E':
        range.append('b' + rest_num)
        range.append('ffffff')
    elif big_num == 'f' or big_num == 'F':
        range.append('b' + rest_num)
        range.append('ffffff')

    return range


def rgb_euclidean_distance(center, p_color):
    center_r = int(center[0:2], 16)
    center_g = int(center[2:4], 16)
    center_b = int(center[4:6], 16)

    p_color_r = int(p_color[0:2], 16)
    p_color_g = int(p_color[2:4], 16)
    p_color_b = int(p_color[4:6], 16)

    return (center_r - p_color_r) ** 2 + \
           (center_g - p_color_g) ** 2 + \
           (center_b - p_color_b) ** 2


def lab_euclidean_distance(center, p_color):
    return (center[0] - p_color[0]) ** 2 + \
           (center[1] - p_color[1]) ** 2 + \
           (center[2] - p_color[2]) ** 2


def p_color_classifier(centroids_result):
    result = []

    for centroid in centroids_result:
        lab = centroid['lab']
        range = range_generator(lab)
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
            if r['type'] == p_color_type and r['subtype'] == p_color_subtype:
                duplicate_flag = 1
                new_ratio = r['ratio'] + ratio
                result[i]['ratio'] = new_ratio
                break
            i += 1

        if duplicate_flag == 0:
            result.append({
                "ratio": ratio,
                "type": p_color_type,
                "subtype": p_color_subtype
            })

    result = sorted(result, key=lambda x: x['ratio'], reverse=True)

    return result

'''
print(p_color_classifier([
    {
        'hex': '#852f44',
        'ratio': 0.1
    },
    {
        'hex': '#852f45',
        'ratio': 0.2
    },
    {
        'hex': '#ffffff',
        'ratio': 0.7
    }
]))
'''