# Handles any functions related to directly reading and writing both bfres and texture data
from io import BytesIO
import clr
import sys
import oead
import pathlib
from PIL import Image
import json
import util

bfresLibPath = pathlib.Path('./src/lib/BfresLibrary/BfresLibrary/bin/Debug/net48').absolute()
sys.path.append(str(bfresLibPath))

def decompressBfres(bfresPath):
    with open(bfresPath, 'rb') as readData:
        decompressedData = oead.yaz0.decompress(readData.read())
    #with open(bfresPath, 'wb') as writeData:
        #writeData.write(decompressedData)
    return decompressedData

def compressBfres(bfresPath):
    with open(bfresPath, 'rb') as readData:
        compressedData = oead.yaz0.compress(readData.read())
    with open(bfresPath, 'wb') as writeData:
        writeData.write(compressedData)
    return

clr.AddReference('BfresLibrary')
clr.AddReference("System.IO")
from BfresLibrary import ResFile
from BfresLibrary.Swizzling import GX2
from BfresLibrary.GX2 import GX2CompSel
from System.IO import MemoryStream, SeekOrigin

#print('imported BfresLibrary texture support successfully')

def changeCulling(bfresPath, outPath=None):
    if not isinstance(bfresPath, pathlib.Path):
        bfresPath = pathlib.Path(bfresPath)
    if (bfresPath.name.split('.')[1] != 'sbfres'):
        return
    for piece in bfresPath.name.split('_'):
        if ('animation' in piece.lower().split('.')):
            return

    try:
        decompBfres = bytearray(decompressBfres(bfresPath))
    except:
        print('failed to decompress file')
        with open(bfresPath, 'rb') as readBfres:
            decompBfres = bytearray(readBfres.read())

    bfresStream = MemoryStream()
    bfresStream.Write(decompBfres, 0, len(decompBfres))
    bfresStream.Seek(0, SeekOrigin.Begin)

    file = ResFile(bfresStream)

    for model in list(file.get_Models()):
        updatedMaterials = []
        #model.get_Value()
        for material in list(model.Value.Materials):
            material.Value.RenderState.PolygonControl.CullFront = True
            material.Value.RenderState.PolygonControl.CullFront = True
            updatedMaterials.append(material)
        #model.Value.Materials = updatedMaterials
    if outPath != None:
        bfresPath = util.findMKDir(f'{outPath}/Model') / bfresPath.name
        file.Save(str(bfresPath.absolute()))
    try:
        compressBfres(bfresPath)
    except:
        print('failed to recompress file')

if __name__ == '__main__':
    changeCulling("C:/Users/drago/Desktop/Relics-Of-The-Past-ORG-Main/Src/content/Model/Enemy_Lynel_Gold_Ancient.sbfres", "C:/Users/drago/Desktop/cullingToZero/assets")