from urllib.parse import unquote_plus
from operator import itemgetter

def reassemble_frags(input_file):
    """
    * make a case to handle if file does not have a new line at the end of the file i.e. /n on last fragment
    :param input_file:
    :return:
    """
    decoded_frags = []
    anchor_frag_index = None
    for i, line in enumerate(input_file):
        decoded_frag = unquote_plus(line[:-1])  # decode & collect each fragment and remove carrier return /n
        decoded_frags.append(decoded_frag)
        if len(decoded_frag) < 15:  # check for a right anchor point with a frag less than 15 characters
            anchor_frag_index = i

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
        # use the right anchor to build to the left
        # find the best match fragment to the right anchor
        matched_frags = {}
        for i, frag in enumerate(decoded_frags):
            if frag[-3:] in anchor_frag:
                matched_frags.update({frag: {'score': 3, 'index': i}})  # fragment will overlap by at least 3 characters
                characters = -4
                while characters > -15:
                    if frag[characters:] in anchor_frag:
                        matched_frags[frag]['score'] += 1
                        characters -= 1
                    else:
                        break

    return decoded_frags, anchor_frag_index


if __name__ == "__main__":
    file = open("frag_files/hello-ordered-frags.txt", "r")
    frags, anchor_index = reassemble_frags(file)
    file.close()
    # max(d1.items(), key=itemgetter(1))[0]
