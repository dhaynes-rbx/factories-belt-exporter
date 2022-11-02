import bpy, os, json
from mathutils.geometry import interpolate_bezier

from bpy.props import IntProperty, FloatProperty

class AT_OP_ExportBelts(bpy.types.Operator):

    bl_idname = "at.export_belts"
    bl_label = "Export Belts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        def get_points(spline, clean=True):
            
            knots = spline.bezier_points
            if len(knots) < 2:
                return

            # verts per segment
            r = spline.resolution_u + 1
            
            # segments in spline
            segments = len(knots)   
            if not spline.use_cyclic_u:
                segments -= 1

            master_point_list = []
            for i in range(segments):
                inext = (i + 1) % len(knots)

                knot1 = knots[i].co
                handle1 = knots[i].handle_right
                handle2 = knots[inext].handle_left
                knot2 = knots[inext].co
                
                bezier = knot1, handle1, handle2, knot2, r
                points = interpolate_bezier(knot1, handle1, handle2, knot2, r)
                master_point_list.extend(points)
                
            # some clean up to remove consecutive doubles, this could be smarter...
            if clean:
                old = master_point_list
                good = [v for i, v in enumerate(old[:-1]) if not old[i] == old[i+1]]
                good.append(old[-1])
                return good
            
            return master_point_list

        def roundNumber(num):
            return round(num, 4)

        def checkForTopMostParent(child):
                if child.parent == None:
                    return child
                else:
                    return checkForTopMostParent(child.parent)

        def checkIfCollectionExists(name):
            checkBool = False
            for collection in bpy.data.collections:
                if collection.name == name:
                    checkBool = True
            return checkBool

        def createOrReplaceCollection(name):
            collectionDoesNotExist = True
            for collection in bpy.data.collections:
                if collection.name == name:
                    for obj in collection.objects:
                        bpy.data.objects.remove(obj, do_unlink = True)
                    collectionDoesNotExist = False
                    return collection
            
            if collectionDoesNotExist:
                #create the collection
                col = bpy.data.collections.new(name)
                bpy.context.scene.collection.children.link(col)
                return col

        def getBeltStartName(obj):
            topMostParent = checkForTopMostParent(obj)
            parentName = topMostParent.name.split(".")[0]
            return parentName

        def getBeltEndName(obj):
            name = ""
            for child in obj.parent.children:
                if getattr(child, 'type') == "EMPTY" and child.name.split()[0] == "End":
                    name = child.name.split()[1].split(".")[0]
            return name

        def getBeltName(obj):
            startName = "(" + getBeltStartName(obj) + ")"
            endName = ""
            if len(getBeltEndName(obj)) > 0:
                endName = "-(" + getBeltEndName(obj) + ")"
            name = startName + endName
            return name

        def exportBeltData():

            # beltsCollection = bpy.data.collections["Belts"]
            if not checkIfCollectionExists("Belts"):
                print("Error! No valid belts exist in this file.")
                return

            beltsCollection = bpy.data.collections["Belts"]
            # Create a collection to hold the empties
            beltDataCollection = createOrReplaceCollection("Belt Location Data")
            
            # Put belt meshes in their own collection, to ease exporting
            filename = os.path.splitext(bpy.path.basename(bpy.context.blend_data.filepath))[0]
            beltMeshCollectionName = "Factories-" + filename + "-BeltMeshes"
            robloxPackageID = ""
            if checkIfCollectionExists(beltMeshCollectionName):
                collection_to_remove = bpy.data.collections.get(beltMeshCollectionName)

                if collection_to_remove["Roblox Package ID"]:
                    robloxPackageID = collection_to_remove["Roblox Package ID"]

                objects_from_collection = [object for object in collection_to_remove.objects]
                bpy.data.collections.remove(collection_to_remove)

            beltMeshCollection = createOrReplaceCollection(beltMeshCollectionName)
            beltMeshCollection["Roblox Package ID"] = robloxPackageID

            beltParents = []
            beltCurves = []
            beltMeshes = []
            for i in range(len(beltsCollection.objects)):
                obj = beltsCollection.objects[i]
                if getattr(obj, 'type') == "EMPTY":
                    if obj == checkForTopMostParent(obj):
                        beltParents.append(obj)
                if getattr(obj, 'type') == 'CURVE':
                    beltCurves.append(obj)
                if getattr(obj, 'type') == 'MESH':
                    beltMeshes.append(obj)
                    obj.name = getBeltName(obj)
                    beltMeshCollection.objects.link(obj)


            # Get the points along the curve and print those to JSON.
            # Create empties so we have a visual representation.
            beltData = "[\n"
            for i in range(len(beltCurves)):
                obj = beltCurves[i]
                if getattr(obj, 'type') != 'CURVE':
                    print("Not a curve!")
                    continue
                
                parentName = getBeltStartName(obj)
                endConnectionName = getBeltEndName(obj)
                beltName = getBeltName(obj)
                
                beltDataJson = ""
                
                spline = obj.data.splines[0]
                points = get_points(spline)
                for j in range(len(points)):
                    v3 = obj.matrix_world @ points[j]
                    pointId = j
                        
                    beltDataJson = {"beltName" : beltName, "pointId": pointId, "position": {"x" : roundNumber(v3.x), "y" : roundNumber(v3.y), "z" : roundNumber(v3.z)}}
            #        beltDataJson = [beltName]
            #        parsed = json.loads(beltDataJson)
                    beltData += json.dumps(beltDataJson, indent = 4) + ",\n"
                    
                    nameStr = "Belt Name: " + beltName + " Point ID: (" + str(i) + "," + str(j) + ")"
                    emptyObj = bpy.data.objects.new(nameStr, None)
                    emptyObj.location = v3
                    
                    emptyObj.parent = obj
                    emptyObj.matrix_parent_inverse = obj.matrix_world.inverted()
                    
                    emptyObj.show_name = True
                    emptyObj.show_in_front = True
                    emptyObj.empty_display_size = .25

                    beltDataCollection.objects.link(emptyObj)

            # get path of the blend file (file should have been saved at least once)
            tempFolder = bpy.path.abspath("//")

            # make a filename
            filename = os.path.join (tempFolder, bpy.path.basename(bpy.context.blend_data.filepath))
            docName = os.path.splitext(filename)[0]
            baseFilename = docName + "-Data.json"
            
            file = open(baseFilename, "w")   # a is for appending  w writes new

            beltData = beltData[:-2] # remove last comma from joined string objects
            beltData = beltData +'\n]'
            file.write(beltData)
            file.close()

            print("Belts Exported")
        
        exportBeltData()
        return {'FINISHED'}