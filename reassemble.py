from urllib.parse import unquote_plus, unquote
from collections import Counter


def find_matches(list_of_fragments, anchor_fragment, fixed_length
                 , verify_left=True, verify_right=True):
    """
    Description:
    Using an anchor fragment find the best matches from the list of fragments to the right, left or left&right.
    -Check how each fragment in the list of fragments fits to the anchor fragment
    -A text file has been fragmented into a series of fixed length substrings which are guaranteed
    to overlap by at least 3 characters and they are guaranteed not to be identical.
    :param list_of_fragments: list[[str]] the list of fragment strings with the anchor fragment removed
    :param anchor_fragment: [str] the anchor fragment string that we are using as a reference for matching
    :param fixed_length: [int] is the most common substring length
    :param verify_left: [boolean] try to find matches to the left of the anchor, defaults to True
    :param verify_right: [boolean] try to find matches to the right of the anchor, defaults to True
    """
    max_overlap = fixed_length - 1 if len(anchor_fragment) >= fixed_length else len(anchor_fragment)
    info = {"anchor": anchor_fragment,
            "num_of_left_matches": 0,
            "left_matches": [],
            "num_of_right_matches": 0,
            "right_matches": [],
            "duplicate": False}
    for i, frag in enumerate(list_of_fragments):   # check every fragment to see if they fit to the anchor fragment
        duplicate_count = 0
        if verify_left:
            for j in range(max_overlap, 2, -1):
                if frag[-j:] == anchor_fragment[:j]:  # check for match left of anchor
                    info["num_of_left_matches"] += 1
                    info["left_matches"].append({"frag": frag, "spliced_frag": frag[:-j]})
                    duplicate_count += 1
                    break
        if verify_right:
            for j in range(max_overlap, 2, -1):
                if anchor_fragment[-j:] == frag[:j]:  # check for match right of anchor
                    info["num_of_right_matches"] += 1
                    info["right_matches"].append({"frag": frag, "spliced_frag": frag[j:]})
                    duplicate_count += 1
                    break
        if duplicate_count == 2:
            info["duplicate"] = True

    return info


def verify_matches(matching_info, list_of_fragments, anchor_fragment, fixed_length, verify_left, verify_right):
    """
    Description:
    verify that a match is perfectly compatible the main anchor frag
    i.e. verify the right side of the left matches to the main anchor frag by guaranteeing
    that only one right side is found and it is the anchor frag and vise versa for the right matches
    :param matching_info: [list[dict]] the list of fragment information that matched with the anchor fragment
    :param list_of_fragments: [list] the list of fragment strings i.e. decoded_frags.copy()
    :param anchor_fragment: [str] the anchor fragment string that needs a match verification
    :param fixed_length: [int] is the most common substring length
    :param verify_left: [boolean] if True will try to find matches to the left of the anchor
    :param verify_right: [boolean] if True will try to find matches to the right of the anchor
    :return: info: [dict] the fragment information that is perfectly compatible or return None
    """
    if len(matching_info) != 0:
        for info in matching_info:
            temp_anchor_frag = info["frag"]
            temp_list_of_fragments = list_of_fragments.copy()
            temp_list_of_fragments.remove(temp_anchor_frag)
            compatible_info = find_matches(temp_list_of_fragments, temp_anchor_frag, fixed_length, verify_left=verify_left, verify_right=verify_right)
            if verify_right and compatible_info["num_of_right_matches"] == 1 and compatible_info['right_matches'][0]['frag'] == anchor_fragment:
                return info
            elif verify_left and compatible_info["num_of_left_matches"] == 1 and compatible_info['left_matches'][0]['frag'] == anchor_fragment:
                return info
    else:
        return None


def assemble_frags(input_file):
    """
    Description:
    reassemble the overlapping fragmented source text
    :param input_file: file object to the fragment txt file
    :return: decoded_frags: [list[str]] the reassembled source text as a string
    """
    decoded_frags = [unquote(line[:-1]) for line in input_file]
    decoded_frags_lengths = [len(frag) for frag in decoded_frags]
    fixed_substring_len = Counter(decoded_frags_lengths).most_common(1)[0][0]
    first_assemble = True
    while first_assemble:
        num_of_fragments = len(decoded_frags)
        for k in range(0, num_of_fragments):
            temp_decoded_frags = decoded_frags.copy()
            main_anchor_frag = temp_decoded_frags.pop(k)
            anchor_match_info = find_matches(temp_decoded_frags, main_anchor_frag, fixed_substring_len)
            combine_frags = main_anchor_frag
            # verify if any matches are perfectly compatible i.e. verify the right side of the left matches to check
            # that only one right side is found and it is the anchor frag
            verified_left_match = verify_matches(anchor_match_info['left_matches'], decoded_frags.copy(), main_anchor_frag, fixed_substring_len, verify_left=False, verify_right=True)
            verified_right_match = verify_matches(anchor_match_info['right_matches'], decoded_frags.copy(), main_anchor_frag, fixed_substring_len, verify_left=True, verify_right=False)
            if verified_left_match is not None and verified_right_match is not None:
                # if the same fragment matches on the left and right of the anchor and it is verified on both sides
                # then move to the next fragment
                if verified_left_match['frag'] == verified_right_match['frag']:
                    continue
            if verified_left_match is not None:
                combine_frags = verified_left_match['spliced_frag'] + combine_frags
                decoded_frags.remove(verified_left_match['frag'])
            if verified_right_match is not None:
                combine_frags = combine_frags + verified_right_match['spliced_frag']
                decoded_frags.remove(verified_right_match['frag'])
            # make sure one of the matches was compatible to replace main_anchor_frag with combine_frags
            if combine_frags != main_anchor_frag:
                decoded_frags.remove(main_anchor_frag)
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
    file = open("frag_files/", "r")
    assemble_fragments = assemble_frags(file)
    print(assemble_fragments[0].replace("+", " "))
    file.close()
