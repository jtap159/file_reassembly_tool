from urllib.parse import unquote_plus, unquote
from collections import Counter


def find_matches(list_of_fragments, anchor_fragment, fixed_length
                 , verify_left=True, verify_right=True):
    """
    first pass
    -Check how each fragment in the list of fragments fits to the anchor fragment
    -A text file has been fragmented into a series of fixed length substrings which are guaranteed
    to overlap by at least 3 characters and they are guaranteed not to be identical.

    * Find the fixed length size of the substrings, but the last substring could be less than the fixed length
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
            print(f"duplicate found with anchor fragment {[anchor_fragment]}")
            info["duplicate"] = True

    return info


def assemble_frags(input_file):
    decoded_frags = [unquote(line[:-1]) for line in input_file]
    decoded_frags_lengths = [len(frag) for frag in decoded_frags]
    fixed_substring_len = Counter(decoded_frags_lengths).most_common(1)[0][0]
    first_pass_matches = {}
    for k in range(0, len(decoded_frags)):
        temp_decoded_frags = decoded_frags.copy()
        anchor_frag = temp_decoded_frags.pop(k)
        anchor_match_info = find_matches(temp_decoded_frags, anchor_frag, fixed_substring_len)
        if anchor_match_info["duplicate"]:
            print(f"duplicate at index {k}")
        matches = {k: anchor_match_info}
        first_pass_matches.update(matches)
    return first_pass_matches


if __name__ == "__main__":
    file = open("frag_files/chopfile-frags.txt", "r")
    anchor_matches = assemble_frags(file)

    # file.close()
