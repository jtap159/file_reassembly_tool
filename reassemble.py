from urllib.parse import unquote_plus, unquote


def assemble_frags(input_file):
    decoded_frags = [unquote(line[:-1]) for line in input_file]  # remove the \n at end of each line, leave +
    while len(decoded_frags) > 1:
        for k in range(0, len(decoded_frags)):  # use every fragment as an anchor and check for how many matches they have
            temp_decoded_frags = decoded_frags.copy()
            anchor_frag = temp_decoded_frags.pop(k)
            max_overlap = 14 if len(anchor_frag) >= 15 else len(anchor_frag)
            num_of_matches_left = 0
            num_of_matches_right = 0
            left_matches = []
            right_matches = []
            for i, frag in enumerate(temp_decoded_frags):  # check every fragment to see if they fit to the anchor fragment
                for j in range(max_overlap, 2, -1):
                    if frag[-j:] == anchor_frag[:j]:  # check for match left of anchor
                        num_of_matches_left += 1
                        left_matches.append({"frag": frag, "spliced_frag": frag[:-j]})  # remove the overlapping characters so it can be combined with the anchor
                        break
                    elif anchor_frag[-j:] == frag[:j]:  # check for match right of anchor
                        num_of_matches_right += 1
                        right_matches.append({"frag": frag, "spliced_frag": frag[j:]})
                        break
            if num_of_matches_left == 1 and num_of_matches_right == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(left_matches[0]['frag'])
                decoded_frags.remove(right_matches[0]['frag'])
                combine_frags = left_matches[0]['spliced_frag'] + anchor_frag + right_matches[0]['spliced_frag']
                decoded_frags.append(combine_frags)
                break
            elif num_of_matches_left == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(left_matches[0]['frag'])
                combine_frags = left_matches[0]['spliced_frag'] + anchor_frag
                decoded_frags.append(combine_frags)
                break
            elif num_of_matches_right == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(right_matches[0]['frag'])
                combine_frags = anchor_frag + right_matches[0]['spliced_frag']
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
    # file_shuffled = open("frag_files/hello-frags.txt", "r")
    # assemble_frags_shuffled = assemble_frags(file_shuffled)[0].replace("+", " ")
    # print('shuffled\n')
    # print(assemble_frags_shuffled)
    # file_shuffled.close()
    file_ordered = open("frag_files/chopfile-frags.txt", "r")
    assemble_frags_ordered = assemble_frags(file_ordered)[0].replace("+", " ")
    print(assemble_frags_ordered)

