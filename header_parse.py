def parse_msg(mystr):
    if mystr[0] == '[':
        print("has a tag")
        tag = mystr.split(']')[0]
        id = tag[1]
        type = tag[2:]
        print (id, type)


mystr = "[Q1] this is an answer"
parse_msg(mystr)

# tag -> A
# id  -> 01
