from urllib.parse import unquote_plus


def reassemble_frags(input_file):
    """
    * make a case to handle if file does not have a new line at the end of the file i.e. /n on last fragment
    :param input_file:
    :return:
    """
    decoded_frags = []
    anchor_frag_index = None
    for i, line in enumerate(input_file):
        decoded_frag = unquote_plus(line[:-1])  # decode each fragment and remove carrier return /n
        decoded_frags.append(decoded_frag)
        if len(decoded_frag) < 15:  # check for a right anchor point with a frag less than 15 characters
            anchor_frag_index = i

    anchor_frag = decoded_frags.pop(0) if anchor_frag_index is None else decoded_frags.pop(anchor_frag_index)

    return decoded_frags, anchor_frag_index


if __name__ == "__main__":
    file = open("frag_files/hello-ordered-frags.txt", "r")
    frags, anchor_index = reassemble_frags(file)
    file.close()
