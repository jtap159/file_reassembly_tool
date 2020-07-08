from urllib.parse import unquote_plus, unquote


def check_matches(list_of_fragments, anchor_fragment):
    """
    Check how each fragment in the list of fragments fits to the anchor fragment
    """
    max_overlap = 14 if len(anchor_fragment) >= 15 else len(anchor_fragment)
    info = {"num_of_left_matches": 0, "left_matches": [],
            "num_of_right_matches": 0, "right_matches": []}
    for i, frag in enumerate(list_of_fragments):  # check every fragment to see if they fit to the anchor fragment
        for j in range(max_overlap, 2, -1):
            if frag[-j:] == anchor_fragment[:j]:  # check for match left of anchor
                info["num_of_left_matches"] += 1
                info["left_matches"].append({"frag": frag, "spliced_frag": frag[:-j]})
                break
            elif anchor_fragment[-j:] == frag[:j]:  # check for match right of anchor
                info["num_of_right_matches"] += 1
                info["right_matches"].append({"frag": frag, "spliced_frag": frag[j:]})
                break
    return info


def number_of_overlap(fragment, left_anchor):
    if len(fragment) > len(left_anchor):
        max_overlap = len(left_anchor)
    else:
        max_overlap = len(fragment)
    num_overlap = 0
    for j in range(max_overlap, 14, -1):
        if left_anchor[-j:] == fragment[:j]:
            num_overlap = j
            break
    return num_overlap


def get_anchors(fragment_list):
    fragment_list_check = fragment_list.copy()
    left_anchor = None
    right_anchor = None
    for fragment in fragment_list:
        fragment_list_check = fragment_list.copy()
        fragment_list_check.remove(fragment)
        matches = check_matches(fragment_list, fragment)
        if left_anchor is None:
            if matches["num_of_left_matches"] == 0:
                left_anchor = fragment
        if right_anchor is None:
            if matches["num_of_right_matches"] == 0:
                right_anchor = fragment
    return left_anchor, right_anchor


def assemble_frags(input_file):
    decoded_frags = [unquote(line[:-1]) for line in input_file]  # remove the \n at end of each line, leave +
    left_end = None
    right_end = None
    anchor_bin = list()
    last_ditch = 0
    while len(decoded_frags) > 1:
        next = 0
        for k in range(0, len(decoded_frags)):
            if next == 1:
                break
            temp_decoded_frags = decoded_frags.copy()
            temp_decoded_frags_anchors = decoded_frags.copy()
            left_anchor, right_anchor = get_anchors(temp_decoded_frags_anchors.copy())    ### !!! can we use global variables for left and right anchor
            if left_anchor is not None:
                temp_decoded_frags_anchors.remove(left_anchor)
                left_anchor_match_info = check_matches(temp_decoded_frags_anchors, left_anchor)
                if left_anchor_match_info["num_of_right_matches"] == 1:
                    left_splice_frag = left_anchor_match_info["right_matches"][0]['spliced_frag']       ### !!!! i would change this to right_splice_frag
                    left_frag = left_anchor_match_info["right_matches"][0]['frag']                      ### !!!! i would change this to right_frag
                    decoded_frags.remove(left_anchor)
                    combine_frags = left_anchor + left_splice_frag
                    decoded_frags.remove(left_frag)
                    decoded_frags.append(combine_frags)
                    if len(anchor_bin) != 0:
                        for anchor in anchor_bin:
                            decoded_frags.append(anchor)
                        anchor_bin = list()
                        break
                    break               ### !!!! i think this break will activate with or without entering the if statement above
                if left_anchor_match_info["num_of_right_matches"] > 1:
                    for anchor_fragment in left_anchor_match_info["right_matches"]:
                        anchor_frag = anchor_fragment["frag"]                           ### !!!! why are we not removing the anchor frag from the temp_decoded_frags it will match with itself
                        anchor_frag_splice = anchor_fragment["spliced_frag"]
                        anchor_match_info = check_matches(temp_decoded_frags, anchor_frag)
                        if anchor_match_info["num_of_left_matches"] == 1:
                            anchor_left_frag = anchor_match_info["left_matches"][0]['frag']
                            if anchor_left_frag == left_anchor:
                                decoded_frags.remove(anchor_frag)
                                combine_frags = left_anchor + anchor_frag_splice
                                decoded_frags.remove(left_anchor)
                                decoded_frags.append(combine_frags)
                                next = 1
                                if len(anchor_bin) != 0:
                                    for anchor in anchor_bin:
                                        decoded_frags.append(anchor)
                                    anchor_bin = list()
                                    break
                                break                                  ### !!!! will need to add an additional break, which means the next = 1 can be removed
            if right_anchor is not None and next == 0:
                temp_decoded_frags_anchors = decoded_frags.copy()
                temp_decoded_frags_anchors.remove(right_anchor)
                right_anchor_match_info = check_matches(temp_decoded_frags_anchors, right_anchor)
                if right_anchor_match_info["num_of_left_matches"] == 1:
                    right_splice_frag = right_anchor_match_info["left_matches"][0]['spliced_frag']
                    right_frag = right_anchor_match_info["left_matches"][0]['frag']
                    decoded_frags.remove(right_anchor)
                    combine_frags = right_splice_frag + right_anchor
                    decoded_frags.remove(right_frag)
                    decoded_frags.append(combine_frags)
                    if len(anchor_bin) != 0:
                        for anchor in anchor_bin:
                            decoded_frags.append(anchor)
                        anchor_bin = list()
                        break
                    break
                if right_anchor_match_info["num_of_left_matches"] > 1:
                    for anchor_fragment in right_anchor_match_info["left_matches"]:
                        anchor_frag = anchor_fragment["frag"]                       ### !!!! why are we not removing the anchor frag from the temp_decoded_frags it will match with itself
                        anchor_frag_splice = anchor_fragment["spliced_frag"]
                        anchor_match_info = check_matches(temp_decoded_frags, anchor_frag)
                        if anchor_match_info["num_of_right_matches"] == 1:
                            anchor_right_frag = anchor_match_info["right_matches"][0]['frag']
                            if anchor_right_frag == right_anchor:
                                decoded_frags.remove(anchor_frag)
                                combine_frags = anchor_frag_splice + right_anchor
                                decoded_frags.remove(right_anchor)
                                decoded_frags.append(combine_frags)
                                next = 1
                                if len(anchor_bin) != 0:
                                    for anchor in anchor_bin:
                                        decoded_frags.append(anchor)
                                    anchor_bin = list()
                                    break
                                break                               ### !!!! will need to add an additional break, which means the next = 1 can be removed
            # find how each fragment in the temp list matches to the anchor frag
            if next != 1:
                anchor_frag = temp_decoded_frags.pop(k)
                anchor_match_info = check_matches(temp_decoded_frags, anchor_frag)
                if anchor_match_info["num_of_left_matches"] == 0:
                    left_end = anchor_frag
                elif anchor_match_info["num_of_right_matches"] == 0:
                    right_end = anchor_frag
                if anchor_match_info["num_of_left_matches"] == 1 and anchor_match_info["num_of_right_matches"] == 1:
                    combine_frags = anchor_frag
                    # first check the left match for compatibility
                    left_compatible = False
                    anchor_left_frag = anchor_match_info['left_matches'][0]['frag']  # make left frag into new anchor
                    temp_decoded_frags = decoded_frags.copy()
                    temp_decoded_frags.remove(anchor_left_frag)
                    left_compatible_info = check_matches(temp_decoded_frags, anchor_left_frag)
                    if left_compatible_info["num_of_right_matches"] == 1 and \
                            left_compatible_info['right_matches'][0]['frag'] == anchor_frag:
                        left_compatible = True
                        left_splice_frag = anchor_match_info["left_matches"][0]['spliced_frag']
                        combine_frags = left_splice_frag + combine_frags
                    # next check the right match for compatibility
                    right_compatible = False
                    anchor_right_frag = anchor_match_info['right_matches'][0]['frag']  # make right frag into new anchor
                    temp_decoded_frags = decoded_frags.copy()
                    temp_decoded_frags.remove(anchor_right_frag)
                    right_compatible_info = check_matches(temp_decoded_frags, anchor_right_frag)
                    if right_compatible_info["num_of_left_matches"] == 1 and \
                            right_compatible_info['left_matches'][0]['frag'] == anchor_frag:
                        right_compatible = True
                        right_splice_frag = anchor_match_info["right_matches"][0]['spliced_frag']
                        decoded_frags.remove(anchor_right_frag)
                        decoded_frags.remove(anchor_left_frag)           ### !!!! this should be in the above if statment in case we only get one side that is perfectly compatible
                        combine_frags = combine_frags + right_splice_frag
                    # make sure one of the matches was compatible to replace anchor_frag with combine_frags
                    if left_compatible and right_compatible:       ### !!!! should this be an "or" condition? because if we have a perfect match on either side of the anchor then we will need to replace the anchor frag with the combine_frags
                        decoded_frags.remove(anchor_frag)
                        decoded_frags.append(combine_frags)
                        if len(anchor_bin) != 0:
                            for anchor in anchor_bin:
                                decoded_frags.append(anchor)
                            anchor_bin = list()
                        break
                    else:
                        if k == len(decoded_frags) - 1:
                            try:
                                decoded_frags.remove(left_end)
                                anchor_bin.append(left_end)
                            except ValueError:
                                decoded_frags.remove(right_end)  ### !!!! what happens if we cannot remove?
                                anchor_bin.append(right_end)
                            # finally:
                            #     decoded_frags.append(left_end)
                            #     anchor_bin.remove(left_end)
                            break
                        # continue
                elif anchor_match_info["num_of_left_matches"] == 1:
                    combine_frags = anchor_frag
                    # check the left match for compatibility
                    left_compatible = False
                    anchor_left_frag = anchor_match_info['left_matches'][0]['frag']  # make left frag into new anchor
                    temp_decoded_frags = decoded_frags.copy()
                    temp_decoded_frags.remove(anchor_left_frag)
                    left_compatible_info = check_matches(temp_decoded_frags, anchor_left_frag)
                    if left_compatible_info["num_of_right_matches"] == 1 and \
                            left_compatible_info['right_matches'][0]['frag'] == anchor_frag:
                        left_compatible = True
                        left_splice_frag = anchor_match_info["left_matches"][0]['spliced_frag']
                        decoded_frags.remove(anchor_left_frag)
                        combine_frags = left_splice_frag + combine_frags
                    # make sure the left match was compatible to replace anchor_frag with combine_frags
                    if left_compatible:                 ### !!! we should be able to combine this if statment with the one above and get rid of the boolean checks
                        decoded_frags.remove(anchor_frag)
                        decoded_frags.append(combine_frags)
                        if len(anchor_bin) != 0:
                            for anchor in anchor_bin:
                                decoded_frags.append(anchor)
                            anchor_bin = list()
                        break
                    else:
                        if k == len(decoded_frags) - 1:
                            print(k)
                            try:
                                # decoded_frags.append(anchor_bin[0])
                                # anchor_bin = list()
                                decoded_frags.remove(left_end)
                                anchor_bin.append(left_end)
                            except ValueError:
                                decoded_frags.remove(right_end)         ### !!!! what happens if we cannot remove?
                                anchor_bin.append(right_end)
                            # finally:
                            #     decoded_frags.append(left_end)
                            #     anchor_bin.remove(left_end)
                            break
                        # continue
                elif anchor_match_info["num_of_right_matches"] == 1:
                    combine_frags = anchor_frag
                    # check the right match for compatibility
                    right_compatible = False
                    anchor_right_frag = anchor_match_info['right_matches'][0]['frag']  # make right frag into new anchor
                    temp_decoded_frags = decoded_frags.copy()
                    temp_decoded_frags.remove(anchor_right_frag)
                    right_compatible_info = check_matches(temp_decoded_frags, anchor_right_frag)
                    if right_compatible_info["num_of_left_matches"] == 1 and \
                            right_compatible_info['left_matches'][0]['frag'] == anchor_frag:
                        right_compatible = True
                        right_splice_frag = anchor_match_info["right_matches"][0]['spliced_frag']
                        decoded_frags.remove(anchor_right_frag)
                        combine_frags = combine_frags + right_splice_frag
                    # make sure the right match was compatible to replace anchor_frag with combine_frags
                    if right_compatible:                    ### !!! we should be able to combine this if statment with the one above and get rid of the boolean checks
                        decoded_frags.remove(anchor_frag)
                        decoded_frags.append(combine_frags)
                        if len(anchor_bin) != 0:
                            for anchor in anchor_bin:
                                decoded_frags.append(anchor)
                            anchor_bin = list()
                        break
                    else:
                        if k == len(decoded_frags) - 1:
                            try:
                                decoded_frags.remove(left_end)
                                anchor_bin.append(left_end)
                            except ValueError:
                                decoded_frags.remove(right_end)             ### !!!! what happens if we cannot remove?
                                anchor_bin.append(right_end)
                            break
                        # continue
                if anchor_match_info["num_of_left_matches"] == 1:
                    combine_frags = anchor_frag
                    anchor_left_frag = anchor_match_info['left_matches'][0]['frag']
                    left_spliced_frag = anchor_match_info['left_matches'][0]['spliced_frag']
                    decoded_frags.remove(anchor_left_frag)
                    decoded_frags.remove(anchor_frag)
                    combine_frags = left_spliced_frag + combine_frags
                    decoded_frags.append(combine_frags)
                    if len(anchor_bin) != 0:
                        for anchor in anchor_bin:
                            decoded_frags.append(anchor)
                        anchor_bin = list()
                    break
                if anchor_match_info["num_of_right_matches"] == 1:
                    combine_frags = anchor_frag
                    anchor_right_frag = anchor_match_info['right_matches'][0]['frag']
                    right_spliced_frag = anchor_match_info['right_matches'][0]['spliced_frag']
                    decoded_frags.remove(anchor_right_frag)
                    decoded_frags.remove(anchor_frag)
                    combine_frags = combine_frags + right_spliced_frag
                    decoded_frags.append(combine_frags)
                    if len(anchor_bin) != 0:
                        for anchor in anchor_bin:
                            decoded_frags.append(anchor)
                        anchor_bin = list()
                    break
                if k == len(decoded_frags) - 1:
                    try:
                        decoded_frags.remove(left_anchor)
                        anchor_bin.append(left_anchor)
                    except ValueError:
                        decoded_frags.remove(right_anchor)
                        anchor_bin.append(right_anchor)
                if len(decoded_frags) <= 3:
                    print('stop')
                    # finally:
                    #     last_ditch = 1
                    #     for anchor in anchor_bin:
                    #         decoded_frags.append(anchor)

    num_overlap_val = number_of_overlap(decoded_frags[0], right_anchor)
    if len(decoded_frags) == 1 and num_overlap_val < 15:
        anchor_frag = decoded_frags[0]
        anchor_match_info = check_matches([left_end, right_end], anchor_frag)
        if anchor_match_info["num_of_left_matches"] == 1 and anchor_match_info["num_of_right_matches"] == 1:
            left_splice_frag = anchor_match_info["left_matches"][0]['spliced_frag']
            right_splice_frag = anchor_match_info["right_matches"][0]['spliced_frag']
            combine_frags = left_splice_frag + anchor_frag + right_splice_frag
            decoded_frags[0] = combine_frags
    return decoded_frags


if __name__ == "__main__":
    # file_ordered = open("frag_files/hello-frags.txt", "r")
    # assemble_frags_ordered = assemble_frags(file_ordered)[0].replace("+", " ")
    # print('ordered\n')
    # print(assemble_frags_ordered)
    # print('\n')
    # file_ordered.close()
    file_shuffled = open("frag_files/chopfile-frags.txt", "r")
    assemble_frags_shuffled = assemble_frags(file_shuffled)[0].replace("+", " ")
    print('shuffled\n')
    print(assemble_frags_shuffled)
    file_shuffled.close()


