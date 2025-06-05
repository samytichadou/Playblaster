import bpy

def get_datapath(datapath):

    # Format for split

    # Remove bracket context
    bracket_list = []
    if "[" in datapath:
        splitted = datapath.split("[")
        for i in range(len(splitted)):
            if not (i % 2) == 0:
                cont = splitted[i].split("]")[0]
                exp = cont
                rep = f"exp2_{i}"
                pair = [
                    rep,
                    exp,
                ]
                bracket_list.append(pair)
                datapath = datapath.replace(f"[{exp}]", rep)

    # Remove "" and '' content
    exp_list = []
    if "'" in datapath:
        splitted = datapath.split("'")
        for i in range(len(splitted)):
            if not (i % 2) == 0:
                exp = f"'{splitted[i]}'"
                rep = f"exp0_{i}"
                pair = [
                    rep,
                    exp,
                ]
                exp_list.append(pair)
                datapath = datapath.replace(exp, rep)

    if '"' in datapath:
        splitted = datapath.split('"')
        for i in range(len(splitted)):
            if not (i % 2) == 0:
                exp = f'"{splitted[i]}"'
                rep = f"exp1_{i}"
                pair = [
                    rep,
                    exp,
                ]
                exp_list.append(pair)
                datapath = datapath.replace(exp, rep)

    # Split
    splitted = datapath.split(".")

    # Reformat
    object_list = []
    for s in splitted:
        if s == "bpy":
            continue
        for rep, exp in exp_list:
            if rep in s:
                s = s.replace(rep, exp)
        object_list.append(s)

    object = bpy

    for s in object_list:

        chk_bracket = False
        for rep, exp in bracket_list:
            if rep in s:
                splitted = s.split(rep)
                if exp.startswith("'") or exp.startswith('"'):
                    exp = exp.replace("'", "").replace('"', "")
                object = getattr(object, splitted[0])[exp]
                chk_bracket = True

        if not chk_bracket:
            object = getattr(object, s)

    return str(object)
