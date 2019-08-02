# template rendering engine

import requests # only needed for API example
import json # only needed for API example

# turns keys into values
def data_library(token, arg_list):
    print("data library received this arg_list:\n" + str(arg_list))
    keys = []
    values = []
    for pair in arg_list:
        pair = pair.split('=')
        keys.append(pair[0])
        values.append(pair[1])

    # all rendering mappings go here
    if token == "author":
        value = "Jake Masters"
    elif token == "pokemon":
        # at this point, we check if the searched_container cookie is set. 
        if "searched_pokemon" not in keys:
            return ""
        else:
            index = keys.index("searched_pokemon")
            api = "https://pokeapi.co/api/v2/pokemon/" + values[index]
            resp = requests.get(url=api)
            try:
                data = resp.json()
                result = "<p>" + values[index] + " was found!</p>\n<img src=\"" + data["sprites"]["front_default"] + "\" alt=\"sprite image\">"  
            except json.decoder.JSONDecodeError:
                result = "<p>The Pokemon you searched for does not exist.</p>"

            return result
    else:
        value = "Value not found."

    return value
    
def replace_tokens(html_stream, token_struct, arg_list):
    # need to do it in reverse for indexing...
    token_struct = token_struct[::-1]
    for entry in token_struct:
        token_start = entry[1]
        token_end = entry[2]
        front_half = html_stream[:token_start]
        back_half = html_stream[token_end+1:]
        print("connecting [0:" + str(token_start) + "] to [" + str(token_end+1) + ":]")

        value = data_library(entry[0], arg_list)

        html_stream = front_half + value + back_half
        print("front half: " + str(front_half[-10:]))
        print("back half: " + str(back_half[0:10]))
    return html_stream

def render(html_stream, arg_list):
    token_struct = []

    # go through html stream
    for i in range(len(html_stream)-2): # don't want to IndexError
        if html_stream[i] == '{' and html_stream[i+1] == '{':
            # a token has been located
            token_string = ""
            token_start = i
            token_end = i
            while html_stream[token_end] != '}' and html_stream[token_end-1] != '}':
                token_end+=1
            token_end+=1
            html_stream_list = list(html_stream)
            reader = token_start
            while reader <= token_end:
                token_string = token_string + html_stream_list[reader]
                reader+=1
            html_stream = "".join(html_stream_list)
            # string {{ }} from token_string
            token_string = token_string.split(' ')[1]
            # add token data to token_struct
            token_struct_entry = []
            token_struct_entry.append(token_string)
            token_struct_entry.append(token_start)
            token_struct_entry.append(token_end)
            token_struct.append(token_struct_entry)

    # pass html_stream into replace_tokens() and assign rendered_html to what replace_tokens() returns
    rendered_html = replace_tokens(html_stream, token_struct, arg_list)

    return rendered_html
