from urllib.parse import unquote_plus, unquote


def find_matches(list_of_fragments, anchor_fragment):
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


def verify_matches(matching_info, list_of_fragments, anchor_fragment):
    """
    verify that a match is perfectly compatible
    :param matching_info: [list[dict]] the list of fragment information that matched with the anchor fragment
    :param list_of_fragments: [list] the list of fragment strings i.e. decoded_frags.copy()
    :param anchor_fragment: [str] the anchor fragment string that need a match verification
    :return: verified_match: [dict] the fragment information that is perfectly compatible
    """
    for info in matching_info:
        temp_anchor_frag = info["frag"]
        list_of_fragments.remove(temp_anchor_frag)
        compatible_info = find_matches(list_of_fragments, temp_anchor_frag)
        if compatible_info["num_of_right_matches"] == 1 and compatible_info['right_matches'][0]['frag'] == anchor_fragment:
            return info
        elif compatible_info["num_of_left_matches"] == 1 and compatible_info['left_matches'][0]['frag'] == anchor_fragment:
            return info
        else:
            return None


def assemble_frags(input_file):
    decoded_frags = [unquote(line[:-1]) for line in input_file]  # remove the \n at end of each line, leave +
    while len(decoded_frags) > 1:
        # check each fragment for left and right matches then check if the matches are perfect
        for k in range(0, len(decoded_frags)):
            temp_decoded_frags = decoded_frags.copy()
            anchor_frag = temp_decoded_frags.pop(k)  # check the last element of the frag list for matches
            anchor_match_info = find_matches(temp_decoded_frags, anchor_frag)
            if anchor_match_info["num_of_left_matches"] >= 1 and anchor_match_info["num_of_right_matches"] >= 1:
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
            elif anchor_match_info["num_of_left_matches"] >= 1 and anchor_match_info["num_of_right_matches"] == 0:
                combine_frags = anchor_frag
                verified_left_match = verify_matches(anchor_match_info['left_matches'], decoded_frags.copy(), anchor_frag)
                if verified_left_match is not None:
                    combine_frags = verified_left_match['spliced_frag'] + combine_frags
                    decoded_frags.remove(verified_left_match['frag'])
                # make sure one of the matches was compatible to replace anchor_frag with combine_frags
                if combine_frags != anchor_frag:
                    decoded_frags.remove(anchor_frag)
                    decoded_frags.append(combine_frags)
                    break
            elif anchor_match_info["num_of_right_matches"] >= 1 and anchor_match_info["num_of_left_matches"] == 0:
                combine_frags = anchor_frag
                verified_right_match = verify_matches(anchor_match_info['right_matches'], decoded_frags.copy(), anchor_frag)
                if verified_right_match is not None:
                    combine_frags = combine_frags + verified_right_match['spliced_frag']
                    decoded_frags.remove(verified_right_match['frag'])
                # make sure one of the matches was compatible to replace anchor_frag with combine_frags
                if combine_frags != anchor_frag:
                    decoded_frags.remove(anchor_frag)
                    decoded_frags.append(combine_frags)
                    break
    return decoded_frags


if __name__ == "__main__":
    # file_ordered = open("frag_files/chopfile-frags.txt", "r")
    # assemble_frags_ordered = assemble_frags(file_ordered)[0].replace("+", " ")
    # print('ordered\n')
    # print(assemble_frags_ordered)
    # print('\n')
    # file_ordered.close()
    file_shuffled = open("frag_files/hello-frags.txt", "r")
    assemble_frags_shuffled = assemble_frags(file_shuffled)[0].replace("+", " ")
    print('shuffled\n')
    print(assemble_frags_shuffled)
    file_shuffled.close()


