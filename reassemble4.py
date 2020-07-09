from urllib.parse import unquote_plus, unquote


def find_matches(list_of_fragments, anchor_fragment, verify_left=True, verify_right=True):
    """
    Check how each fragment in the list of fragments fits to the anchor fragment
    """
    max_overlap = 14 if len(anchor_fragment) >= 15 else len(anchor_fragment)
    info = {"num_of_left_matches": 0, "left_matches": [],
            "num_of_right_matches": 0, "right_matches": []}
    for i, frag in enumerate(list_of_fragments):  # check every fragment to see if they fit to the anchor fragment
        found_match = False
        for j in range(max_overlap, 2, -1):
            if frag[-j:] == anchor_fragment[:j]:  # check for match left of anchor
                info["num_of_left_matches"] += 1
                info["left_matches"].append({"frag": frag, "spliced_frag": frag[:-j]})
                found_match = True
            if anchor_fragment[-j:] == frag[:j]:  # check for match right of anchor       ### !!!!  is breaking after finding the left match causing issues? should we allow the right to be checked too
                info["num_of_right_matches"] += 1                                           ### !!! i tried having the right be check even if a left match is found at that j value and cause a .remove() later in the code
                info["right_matches"].append({"frag": frag, "spliced_frag": frag[j:]})
                found_match = True
            if found_match:
                break
    return info


def verify_matches(matching_info, list_of_fragments, anchor_fragment, verify_left=True, verify_right=True):
    """
    verify that a match is perfectly compatible
    :param matching_info: [list[dict]] the list of fragment information that matched with the anchor fragment
    :param list_of_fragments: [list] the list of fragment strings i.e. decoded_frags.copy()
    :param anchor_fragment: [str] the anchor fragment string that need a match verification
    :return: verified_match: [dict] the fragment information that is perfectly compatible
    """
    if len(matching_info) != 0:
        for info in matching_info:
            temp_anchor_frag = info["frag"]
            temp_list_of_fragments = list_of_fragments.copy()
            temp_list_of_fragments.remove(temp_anchor_frag)
            compatible_info = find_matches(temp_list_of_fragments, temp_anchor_frag, verify_left, verify_right)
            if compatible_info["num_of_right_matches"] == 1 and compatible_info['right_matches'][0]['frag'] == anchor_fragment:
                return info
            elif compatible_info["num_of_left_matches"] == 1 and compatible_info['left_matches'][0]['frag'] == anchor_fragment:
                return info
    else:
        return None


def assemble_frags(input_file):
    decoded_frags = [unquote(line[:-1]) for line in input_file]  # remove the \n at end of each line, leave +
    first_assemble = True
    while first_assemble:
        # check each fragment for left and right matches then check if the matches are perfect
        num_of_fragments = len(decoded_frags)
        for k in range(0, num_of_fragments):
            temp_decoded_frags = decoded_frags.copy()
            anchor_frag = temp_decoded_frags.pop(k)  # check the last element of the frag list for matches
            anchor_match_info = find_matches(temp_decoded_frags, anchor_frag)
            combine_frags = anchor_frag
            verified_left_match = verify_matches(anchor_match_info['left_matches'], decoded_frags.copy(), anchor_frag)
            verified_right_match = verify_matches(anchor_match_info['right_matches'], decoded_frags.copy(), anchor_frag)
            if verified_left_match is not None:
                combine_frags = verified_left_match['spliced_frag'] + combine_frags
                decoded_frags.remove(verified_left_match['frag'])
            if verified_right_match is not None:
                combine_frags = combine_frags + verified_right_match['spliced_frag']
                decoded_frags.remove(verified_right_match['frag'])
            # make sure one of the matches was compatible to replace anchor_frag with combine_frags
            if combine_frags != anchor_frag:
                decoded_frags.remove(anchor_frag)
                decoded_frags.append(combine_frags)
                break
            elif k == num_of_fragments - 1:
                print("No more perfect matches can be found")
                first_assemble = False
        if len(decoded_frags) == 1:
            print("Assembly Finished!")
            first_assemble = False
    return decoded_frags


if __name__ == "__main__":
    # file_ordered = open("frag_files/Shake-frags.txt", "r")
    # assemble_frags_ordered = assemble_frags(file_ordered)
    # print(assemble_frags_ordered)
    # file_ordered.close()
    file_shuffled = open("frag_files/hello-ordered-frags.txt", "r")
    assemble_frags_shuffled = assemble_frags(file_shuffled)[0].replace("+", " ")
    print(assemble_frags_shuffled)
    file_shuffled.close()


