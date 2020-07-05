from urllib.parse import unquote_plus
from operator import itemgetter
import pandas as pd


def decode_frags(input_file):
    decoded_frags = []
    anchor_frag_index = None
    for i, line in enumerate(input_file):
        decoded_frag = unquote_plus(line[:-1])  # decode & collect each fragment and remove carrier return /n
        decoded_frags.append(decoded_frag)
        if len(decoded_frag) < 15:  # check for a right anchor point with a frag less than 15 characters
            anchor_frag_index = i
    return decoded_frags, anchor_frag_index


def reassemble_frags(input_file):
    """
    * make a case to handle if file does not have a new line at the end of the file i.e. /n on last fragment
    :param input_file:
    :return:
    """
    decoded_frags, anchor_frag_index = decode_frags(input_file)
    # the starting point for reassembling the fragments
    # if anchor_frag_index is not None value then the anchor fragment is the last fragment (a.k.a. right anchor)
    # if no fragment with less than 15 characters is found then the first fragment in decoded_frags will be the anchor
    if anchor_frag_index is not None:
        anchor_frag = decoded_frags.pop(anchor_frag_index)
        right_anchor = True
    else:
        anchor_frag = decoded_frags.pop(0)
        right_anchor = False

    if right_anchor:
        reassembled_string = anchor_frag
        # use the right anchor to build to the left
        for j in range(0, 3):
            # find the best match fragment to the right anchor
            matched_frags = []
            for i, frag in enumerate(decoded_frags):
                # The right side of a fragment will match with the "right" anchor
                if frag[-3:] in anchor_frag:
                    num_of_characters = -4
                    while num_of_characters > -15:
                        if frag[num_of_characters:] in anchor_frag:
                            num_of_characters -= 1
                        else:
                            # found how many characters overlap, calculate score
                            matched_frags.append({'overlap': num_of_characters + 1, 'frag_index': i})
                            break
            df = pd.DataFrame(matched_frags)
            df.sort_values(by='overlap', ascending=True, ignore_index=True, inplace=True)
            max_overlap = df.loc[0, 'overlap']
            # need to add a condition for this situation when multiple fragments have the same max score
            if len(df[df['overlap'] == max_overlap]) > 1:
                print("this will be a problem")
            best_match_index = df.loc[0, 'frag_index']
            best_match_frag = decoded_frags.pop(best_match_index)
            anchor_frag = best_match_frag  # keep working to the left
            reassembled_string = best_match_frag[:max_overlap] + reassembled_string


    return decoded_frags, anchor_frag_index


if __name__ == "__main__":
    file = open("frag_files/hello-ordered-frags.txt", "r")
    frags, anchor_index = reassemble_frags(file)
    file.close()
    # max(d1.items(), key=itemgetter(1))[0]
