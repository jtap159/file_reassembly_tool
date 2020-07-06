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
    while len(decoded_frags) > 1:
        for k in range(0, len(decoded_frags)):
            temp_decoded_frags = decoded_frags.copy()
            anchor_frag = temp_decoded_frags.pop(k)
            # find how each fragment in the temp list matches to the anchor frag
            anchor_match_info = check_matches(temp_decoded_frags, anchor_frag)
            if anchor_match_info["num_of_left_matches"] == 1 and anchor_match_info["num_of_right_matches"] == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(anchor_match_info["left_matches"][0]['frag'])
                decoded_frags.remove(anchor_match_info["right_matches"][0]['frag'])
                left_splice_frag = anchor_match_info["left_matches"][0]['spliced_frag']
                right_splice_frag = anchor_match_info["right_matches"][0]['spliced_frag']
                combine_frags = left_splice_frag + anchor_frag + right_splice_frag
                decoded_frags.append(combine_frags)
                break
            elif anchor_match_info["num_of_left_matches"] == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(anchor_match_info["left_matches"][0]['frag'])
                left_splice_frag = anchor_match_info["left_matches"][0]['spliced_frag']
                combine_frags = left_splice_frag + anchor_frag
                decoded_frags.append(combine_frags)
                break
            elif anchor_match_info["num_of_right_matches"] == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(anchor_match_info["right_matches"][0]['frag'])
                right_splice_frag = anchor_match_info["right_matches"][0]['spliced_frag']
                combine_frags = anchor_frag + right_splice_frag
                decoded_frags.append(combine_frags)
                break
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


