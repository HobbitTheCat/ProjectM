arr = [{"id": 1, "parent_id": None, "name": "L2"},
       {"id": 2, "parent_id": None, "name": "MI4"},
       {"id": 3, "parent_id": None, "name": "IE4"},
       {"id": 4, "parent_id": None, "name": "MI4-FC"},
       {"id": 5, "parent_id": None, "name": "MI4-06"},
       {"id": 6, "parent_id": None, "name": "MI4-061"},
       {"id": 7, "parent_id": None, "name": "MI4-062"},
       {"id": 8, "parent_id": None, "name": "IE4-I"},
       {"id": 9, "parent_id": None, "name": "IE4-I4"},
       {"id": 10, "parent_id": None, "name": "IE4-I41"},
       {"id": 11, "parent_id": None, "name": "IE4-I42"},
       {"id": 12, "parent_id": None, "name": "L3"}]

def getListIdDown(array, index):
    exitList = []
    for item in array:
        if item["parent_id"] == index:
            exitList.append(item)
    return exitList
def getIdUp(array, index):
    for item in array:
        if item["id"] == index:
            return item
    return None

def moveToNextLayer(dictionList):
    for diction in dictionList:
        parentId = None
        for group in arr:
            if group["name"] == diction["p"]:
                parentId = group["id"]
        for i in range(len(arr)):
            if arr[i]["name"] in diction["g"]:
                arr[i]["parent_id"] = parentId

def getGroupDown(array, groupId, exitList = None):
    if exitList is None:
        exitList = []
    subgroupList = getListIdDown(array, groupId)
    exitList.extend(subgroupList)
    for subgroup in subgroupList:
        exitList.extend(getGroupDown(array, subgroup["id"]))
    return exitList

def getGroupUp(array, groupId, exitList = None):
    if exitList is None:
        exitList = []
    upId = getIdUp(array, groupId)
    exitList.append(upId)
    if upId["parent_id"] is None:
        return exitList

    return getGroupUp(array, upId["parent_id"], exitList)

def imageRec(currentLevelElls, level = 0):
    for ell in currentLevelElls:
        print(" |" * level, end="")
        print(f"-{ell["name"]}, id: {ell['id']}")
        imageRec([item for item in arr if item["parent_id"] == ell["id"]], level + 1)

moveToNextLayer([{"g":["MI4","IE4"], "p":"L2"},
                 {"g":["MI4-FC","MI4-06"], "p":"MI4"},
                 {"g":["MI4-061","MI4-062"], "p":"MI4-06"},
                 {"g":["IE4-I"], "p":"IE4"},
                 {"g":["IE4-I4"], "p":"IE4-I"},
                 {"g":["IE4-I41","IE4-I42"], "p":"IE4-I4"}])
root = [ell for ell in arr if ell["parent_id"] is None]
imageRec(root)
print(getGroupDown(arr, 1))
print(getGroupUp(arr, 10))
