from urllib.parse import unquote_plus, unquote
from collections import Counter
import numpy as np


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
    decoded_frags = [unquote_plus(line[:-1]) for line in input_file]
    decoded_frags_lengths = [len(frag) for frag in decoded_frags]
    fixed_substring_len = Counter(decoded_frags_lengths).most_common(1)[0][0]
    first_assemble = True
    while first_assemble:
        no_matches_info = []
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
            if verified_left_match is None and verified_right_match is None:
                no_matches_info.append(anchor_match_info)
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
                print("No more perfect matches can be found...checking permutations")
                assembled_permutations = find_best_combination(no_matches_info, decoded_frags, fixed_substring_len)
                return assembled_permutations
        if len(decoded_frags) == 1:
            print("Assembly Finished!")
            first_assemble = False
    return decoded_frags


def find_left_anchor_index(fragment_info, fragments):
    for info in fragment_info:
        if len(info['left_matches']) == 0:
            return fragments.index(info['anchor'])


def create_matching_matrix(fragment_info, fragments):
    # building to the right, so use the right matches of each fragment info
    # rows are building to the right
    # columns are building to the left
    matching_matrix = np.zeros((len(fragments), len(fragments)), dtype=np.int32)
    for info in fragment_info:
        row_index = fragments.index(info['anchor'])
        column_indexes = [fragments.index(right_match['frag']) for right_match in info['right_matches']]
        for column_index in column_indexes:
            matching_matrix[row_index][column_index] = 1
    return matching_matrix


def create_tracker_array(frags_used):
    # create a binary array to track what fragments have been used
    tracker_array = np.ones(13, dtype=np.int32)
    for frag_used in frags_used:
        tracker_array[frags_used] = 0
    return tracker_array


def find_best_combination(fragments_info, fragments, fixed_len):
    matching_matrix = create_matching_matrix(fragments_info, fragments)
    left_anchor_index = find_left_anchor_index(fragments_info, fragments)
    # use the left anchor as the starting point (first slot)
    frags_permutation = [left_anchor_index]
    slot_tracker_array = create_tracker_array(frags_permutation)
    # now find all the possible matches to the right of the left anchor
    right_matching_bin = matching_matrix[left_anchor_index, :] * slot_tracker_array
    right_matching_indices = np.where(right_matching_bin == 1)[0].tolist()
    # create an empty list of lists for tacking the right matches
    right_matching_tracker = [[] for i in range(0, len(matching_matrix))]
    right_matching_tracker[0] = right_matching_indices

    possible_permutations = []
    rm_index = 0  # right match index
    add_matches_index = 1  # add the right matches to the right match tracker
    while len(right_matching_tracker[rm_index]) != 0 and rm_index >= 0:
        select_frag = right_matching_tracker[rm_index][0]
        frags_permutation.append(select_frag)
        slot_tracker_array = create_tracker_array(frags_permutation)
        right_matching_bin = matching_matrix[select_frag, :] * slot_tracker_array
        right_matching_indices = np.where(right_matching_bin == 1)[0].tolist()
        if len(right_matching_indices) == 0:
            possible_permutations.append(frags_permutation.copy())
            frags_permutation.pop()  # go back one slot
            del right_matching_tracker[rm_index][0]
            while len(right_matching_tracker[rm_index]) == 0:
                rm_index -= 1
                add_matches_index -= 1
                frags_permutation.pop()
                if rm_index < 0:
                    break
                del right_matching_tracker[rm_index][0]
            continue
        right_matching_tracker[add_matches_index] = right_matching_indices
        # pick fragment from the right matching indices
        rm_index += 1
        add_matches_index += 1
    assembled_permutations = assemble_permutations(possible_permutations, fragments, fixed_len, left_anchor_index)
    return assembled_permutations


def assemble_permutations(permutations, fragments, fixed_length, left_anchor_index):
    # need to add parenthesis check and tab auto-correct
    # all the fragments should be greater than or equal to the fixed length at this point
    max_overlap = fixed_length - 1
    complete_fragment_size = len(fragments)
    # from the permutations we use the left anchor as the starting point every time assuming we found the left anchor
    assemblies = []
    for permutation in permutations:
        if len(permutation) == complete_fragment_size:
            assembly = fragments[left_anchor_index]
            del permutation[0]
            for i in permutation:
                for j in range(max_overlap, 2, -1):
                    if assembly[-j:] == fragments[i][:j]:  # check for match right of anchor
                        assembly = assembly + fragments[i][j:]
                        break
            validate = validate_parantheses(assembly)
            if validate:
                assemblies.append(assembly)
    all_scores = []
    for assembly in assemblies:
        space_scoring = score_spaces(assembly)
        all_scores.append(space_scoring)

    best_score_index = [i for i, value in enumerate(all_scores) if value == 1]
    final_assemblies = []
    for k in best_score_index:
        final_assemblies.append(assemblies[k])
    return final_assemblies


def validate_parantheses(document):
    # build the sequence of parantheses found in the document
    list_of_parantheses = ["(", ")", "[", "]", "{", "}"]
    check_parantheses = ''
    for character in document:
        if character in list_of_parantheses:
            check_parantheses += character
    stack, pchar = [], {"(": ")", "{": "}", "[": "]"}
    for parenthese in check_parantheses:
        if parenthese in pchar:
            stack.append(parenthese)
        elif len(stack) == 0 or pchar[stack.pop()] != parenthese:
            return False
    return len(stack) == 0


def score_spaces(document):
    # the more positive the score the more spacing issues occurred
    valid_spacing = [1, 4, 8, 12, 16]
    count = 0
    check = []
    for character in document:
        if character == " ":
            count += 1
        elif count > 0:
            check.append(count)
            count = 0
    score = 0
    for spacing in check:
        if spacing not in valid_spacing:
            min_score = min([abs(i - spacing) for i in valid_spacing])
            score += min_score
    return score


if __name__ == "__main__":
    file = open("frag_files/hello-ordered-frags.txt", "r")
    assembled_perms = assemble_frags(file)
    file.close()


