from collections import Counter
import numpy as np


def validate_parentheses(document):
    """
    Description:
    Used to check if a document has the proper use of parentheses
    :param document: [str] a document represented as a single string
    :return: True if document has proper use of parentheses or False if the document does not have proper parentheses
    """
    # build the sequence of parentheses found in the document
    list_of_parentheses = ["(", ")", "[", "]", "{", "}"]
    check_parentheses = ''
    for character in document:
        if character in list_of_parentheses:
            check_parentheses += character
    stack, pchar = [], {"(": ")", "{": "}", "[": "]"}
    for parenthesis in check_parentheses:
        if parenthesis in pchar:
            stack.append(parenthesis)
        elif len(stack) == 0 or pchar[stack.pop()] != parenthesis:
            return False
    return len(stack) == 0


def assemble_permutations(permutations, fragments, fixed_length, left_anchor_index):
    """
    Description:
    Assemble the provided permutations. the permutations are a list of fragment index values so the fragments
    are found using the index then assembling by their appropriate overlap. has similar logic to find_matches().
    Only assemble the permutations that have all of the fragments and that have proper use of parentheses.
    :param permutations: [list[list[str]]] the list of all the possible permutations
    :param fragments: [list[str]] the list of fragments that can not be matched
    :param fixed_length: [int] is the most common substring length
    :param left_anchor_index: [int] the index location in the fragment list for the left anchor fragment
    :return: assemblies [list[str]] a list of the best possible reassembles
    """
    # all the fragments should be greater than or equal to the fixed length at this point
    max_overlap = fixed_length - 1
    complete_fragment_size = len(fragments)
    # from the permutations we use the left anchor as the starting point every time assuming we found the left anchor
    space_check = set(" ")
    acceptable_spaces = [4, 8, 12, 16]
    assemblies = []
    for permutation in permutations:
        if len(permutation) == complete_fragment_size:
            assembly = fragments[left_anchor_index]
            del permutation[0]  # remove left anchor from assembly list
            for i in permutation:
                frag = fragments[i]
                for j in range(max_overlap, 2, -1):
                    anchor_overlap = assembly[-j:]
                    right_overlap = frag[:j]
                    spliced_frag = frag[j:]
                    if anchor_overlap == right_overlap:  # check for match right of anchor
                        if set(right_overlap) == space_check:
                            anchor_spaces = 0
                            frag_spaces = 0
                            for k in range(len(assembly)-1, 0, -1):
                                if assembly[k] == " ":
                                    anchor_spaces += 1
                                else:
                                    break
                            for k in range(0, len(spliced_frag)):
                                if spliced_frag[k] == " ":
                                    frag_spaces += 1
                                else:
                                    break
                            total_spaces = anchor_spaces + frag_spaces
                            if total_spaces in acceptable_spaces:
                                assembly = assembly + frag[j:]
                                break
                            else:
                                continue
                        assembly = assembly + frag[j:]
                        break
            validate = validate_parentheses(assembly)
            if validate:
                assemblies.append(assembly)
    return assemblies


def create_tracker_array(frags_used):
    """
    Description:
    Used to determine which fragments have been used so far when assembling a permutation.
    Multiplying the tracker array by a row of the matching matrix will give the available fragments
    that can be used to build to the right
    :param frags_used: [list[int]] a list of the fragment indexes used for a permutation
    :return: tracker_array [ndarray] a binary array to track what fragments have been used
    """
    tracker_array = np.ones(13, dtype=np.int32)
    for frag_used in frags_used:
        tracker_array[frags_used] = 0
    return tracker_array


def find_left_anchor_index(fragment_info, fragments):
    """
    Description:
    Use the fragment information to find which fragment is the left anchor
    :param fragment_info: [list[dict]] the list of fragment information
    :param fragments: [list] the list of fragments being searched
    :return: left_anchor_index: [int] the index location in the fragment list for the left anchor fragment
    """
    for info in fragment_info:
        if len(info['left_matches']) == 0:
            left_anchor_index = fragments.index(info['anchor'])
            return left_anchor_index


def create_matching_matrix(fragment_info, fragments):
    """
    Description:
    This function creates a matrix that can be used to identify how fragments match with one another
    :param fragment_info: [list[dict]] the fragment information for the fragments that can not be matched
    :param fragments: [list[str]] the list of fragments that can not be matched
    :return: matching_matrix [ndarray] a binary matrix that describes how fragments match with one another
    """
    # rows are used if building to the right of an anchor
    # columns are used if building to the left of an anchor
    # building to the right, so use the right matches of each fragment info
    matching_matrix = np.zeros((len(fragments), len(fragments)), dtype=np.int32)
    for info in fragment_info:
        row_index = fragments.index(info['anchor'])
        column_indexes = [fragments.index(right_match['frag']) for right_match in info['right_matches']]
        for column_index in column_indexes:
            matching_matrix[row_index][column_index] = 1
    return matching_matrix


def find_best_combination(fragments_info, fragments, fixed_len):
    """
    Description:
    This function is used when the decoded fragments no longer have anymore perfect matches.
    the fragments are assembled for every permutation using the left anchor fragment as a reference.
    based on matching conditions in fragments_info the best possible reassembles
    will be ones that use all of the fragments and have proper parentheses.
    :param fragments_info: [list[dict]] the fragment information for the fragments that can not be matched
    :param fragments: [list[str]] the list of fragments that can not be matched
    :param fixed_len: [int] is the most common substring length
    :return: assembled_permutations [list[str]] a list of the best possible reassembles
    """
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


def verify_matches(matching_info, list_of_fragments, anchor_fragment, fixed_length, verify_left, verify_right):
    """
    Description:
    verify that a match is perfectly compatible to the main anchor frag
    i.e. one of the left matches has only one right side match and it is the main_anchor_frag
    and vice versa for right matches
    :param matching_info: [list[dict]] the list of fragment matches found for the anchor fragment
    :param list_of_fragments: [list[str]] the list of fragment strings i.e. decoded_frags.copy()
    :param anchor_fragment: [str] the anchor fragment string that needs a match verification
    :param fixed_length: [int] is the most common substring length
    :param verify_left: [boolean] if True will try to find matches to the left of the reference anchor
    :param verify_right: [boolean] if True will try to find matches to the right of the reference anchor
    :return: info: [dict] the fragment information that is perfectly compatible or return None
    """
    if len(matching_info) != 0:
        for info in matching_info:
            temp_anchor_frag = info["frag"]
            temp_list_of_fragments = list_of_fragments.copy()
            temp_list_of_fragments.remove(temp_anchor_frag)
            compatible_info = find_matches(temp_list_of_fragments, temp_anchor_frag, fixed_length,
                                           verify_left=verify_left, verify_right=verify_right)
            if verify_right and compatible_info["num_of_right_matches"] == 1 and \
                    compatible_info['right_matches'][0]['frag'] == anchor_fragment:
                return info
            elif verify_left and compatible_info["num_of_left_matches"] == 1 and \
                    compatible_info['left_matches'][0]['frag'] == anchor_fragment:
                return info
    else:
        return None


def find_matches(list_of_fragments, anchor_fragment, fixed_length
                 , verify_left=True, verify_right=True):
    """
    Description:
    Using an anchor fragment find the best matches from the list of fragments to the right, left or left&right
    of the anchor fragment.
    :param list_of_fragments: list[[str]] the list of fragment strings with the anchor fragment removed
    :param anchor_fragment: [str] the anchor fragment string that we are using as a reference for matching
    :param fixed_length: [int] is the most common substring length
    :param verify_left: [bool] try to find matches to the left of the anchor, defaults to True
    :param verify_right: [bool] try to find matches to the right of the anchor, defaults to True
    """
    max_overlap = fixed_length - 1 if len(anchor_fragment) >= fixed_length else len(anchor_fragment)
    info = {"anchor": anchor_fragment,
            "num_of_left_matches": 0,
            "left_matches": [],
            "num_of_right_matches": 0,
            "right_matches": [],
            "duplicate": False}
    space_check = set(" ")
    acceptable_spaces = [4, 8, 12, 16]
    for i, frag in enumerate(list_of_fragments):   # check every fragment to see if they fit to the anchor fragment
        duplicate_count = 0
        if verify_left:  # check for matches left of the anchor
            for j in range(max_overlap, 2, -1):
                anchor_overlap = anchor_fragment[:j]
                left_overlap = frag[-j:]
                spliced_frag = frag[:-j]
                if left_overlap == anchor_overlap:
                    if set(left_overlap) == space_check:  # check if the overlap is only spaces
                        anchor_spaces = 0
                        frag_spaces = 0
                        for k in range(len(spliced_frag)-1, 0, -1):
                            if spliced_frag[k] == " ":
                                frag_spaces += 1
                            else:
                                break
                        for k in range(0, len(anchor_fragment)):
                            if anchor_fragment[k] == " ":
                                anchor_spaces += 1
                            else:
                                break
                        total_spaces = frag_spaces + anchor_spaces
                        if total_spaces in acceptable_spaces:
                            info["num_of_left_matches"] += 1
                            info["left_matches"].append({"frag": frag, "spliced_frag": spliced_frag})
                            duplicate_count += 1
                            break
                        else:
                            continue
                    info["num_of_left_matches"] += 1
                    info["left_matches"].append({"frag": frag, "spliced_frag": spliced_frag})
                    duplicate_count += 1
                    break
        if verify_right:  # check for matches right of the anchor
            for j in range(max_overlap, 2, -1):
                anchor_overlap = anchor_fragment[-j:]
                right_overlap = frag[:j]
                spliced_frag = frag[j:]
                if anchor_overlap == right_overlap:
                    if set(right_overlap) == space_check:  # check if the overlap is only spaces
                        anchor_spaces = 0
                        frag_spaces = 0
                        for k in range(len(anchor_fragment)-1, 0, -1):
                            if anchor_fragment[k] == " ":
                                anchor_spaces += 1
                            else:
                                break
                        for k in range(0, len(spliced_frag)):
                            if spliced_frag[k] == " ":
                                frag_spaces += 1
                            else:
                                break
                        total_spaces = anchor_spaces + frag_spaces
                        if total_spaces in acceptable_spaces:
                            # the total spaces need to be a tab worth of spaces i.e. 4, 8, 12 etc..
                            info["num_of_right_matches"] += 1
                            info["right_matches"].append({"frag": frag, "spliced_frag": spliced_frag})
                            duplicate_count += 1
                            break
                        else:
                            continue
                    info["num_of_right_matches"] += 1
                    info["right_matches"].append({"frag": frag, "spliced_frag": spliced_frag})
                    duplicate_count += 1
                    break
        if duplicate_count == 2:
            info["duplicate"] = True

    return info


def assemble_frags(decoded_frags):
    """
    Description:
    Used to reassemble a text file that has been fragmented into a series of fixed length substrings
    which are guaranteed to overlap by at least 3 characters and not to be identical.
    The final fragment is likely to have less characters than the other substrings.
    The order of the fragments can also be shuffled.
    :param decoded_frags: [list[str]] the list of fragments that have already been URL decoded

    --if the permutations were narrowed down to one solution
    :return: reassembled_file: [str] the fragments reassembled and combined into a string

    --if multiple permutations are all viable solutions based on the constraints
    :return: assembled_permutations: [list[str]] list of the different reassembled fragment solutions
    """
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
            # verify if any matches are perfectly compatible i.e. that one of the left matches has only
            # one right side match and it is the main_anchor_frag and vice versa for right matches
            verified_left_match = verify_matches(anchor_match_info['left_matches'], decoded_frags.copy(),
                                                 main_anchor_frag, fixed_substring_len,
                                                 verify_left=False, verify_right=True)
            verified_right_match = verify_matches(anchor_match_info['right_matches'], decoded_frags.copy(),
                                                  main_anchor_frag, fixed_substring_len,
                                                  verify_left=True, verify_right=False)
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
                #  if none of the fragments have perfect matches then find all of the remaining permutations
                assembled_permutations = find_best_combination(no_matches_info, decoded_frags, fixed_substring_len)
                return assembled_permutations
        if len(decoded_frags) == 1:
            first_assemble = False
    reassembled_file = decoded_frags[0]
    return reassembled_file


if __name__ == "__main__":
    from urllib.parse import unquote_plus
    with open("../frag_files/hello-ordered-frags.txt", 'r') as file:
        file_fragments = [unquote_plus(line[:-1]) for line in file]
    assembled_fragments = assemble_frags(file_fragments)
