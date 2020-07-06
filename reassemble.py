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


def assemble_frags(input_file):
    decoded_frags = [unquote(line[:-1]) for line in input_file]  # remove the \n at end of each line, leave +
    left_end = None
    right_end = None
    while len(decoded_frags) > 1:
        for k in range(0, len(decoded_frags)):
            temp_decoded_frags = decoded_frags.copy()
            anchor_frag = temp_decoded_frags.pop(k)
            # find how each fragment in the temp list matches to the anchor frag
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
                    decoded_frags.remove(anchor_left_frag)
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
                    combine_frags = combine_frags + right_splice_frag
                # make sure one of the matches was compatible to replace anchor_frag with combine_frags
                if left_compatible or right_compatible:
                    decoded_frags.remove(anchor_frag)
                    decoded_frags.append(combine_frags)
                    break
                else:
                    continue
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
                if left_compatible:
                    decoded_frags.remove(anchor_frag)
                    decoded_frags.append(combine_frags)
                    break
                else:
                    continue
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
                if right_compatible:
                    decoded_frags.remove(anchor_frag)
                    decoded_frags.append(combine_frags)
                    break
                else:
                    continue
            if k == len(decoded_frags) - 1:
                decoded_frags.remove(left_end)
                decoded_frags.remove(right_end)
    return decoded_frags


if __name__ == "__main__":
    # file_ordered = open("frag_files/hello-ordered-frags.txt", "r")
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


