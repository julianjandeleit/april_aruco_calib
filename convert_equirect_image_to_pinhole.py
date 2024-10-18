import numpy as np
from PIL import Image
from omnicv import fisheyeImgConv
import math

def convert(inname, outname,deg_x):

    equiRect = np.array(Image.open(inname))

    outShape = [400, 400]
    inShape = equiRect.shape[:2]
    mapper = fisheyeImgConv()
    FOV = 90
    Theta = 45 # horizontal shift
    Phi = 0 # vertical shift in deg
    Hd = outShape[0]
    Wd = outShape[1]
    np.bool = np.bool_
    np.float = np.float64
    persp = mapper.eqruirect2persp(equiRect, FOV, Theta, Phi, Hd, Wd)

    def get_block(equiRect, FOV=90, Theta=0, Phi = 0, outShape = [800, 800]):
        inShape = equiRect.shape[:2]
        mapper = fisheyeImgConv()
        #FOV = 90
        #Theta = 45 # horizontal shift
        #Phi = 0 # vertical shift in deg
        Hd = outShape[0]
        Wd = outShape[1]
        import numpy as np
        np.bool = np.bool_
        np.float = np.float64
        persp = mapper.eqruirect2persp(equiRect, FOV, Theta, Phi, Hd, Wd)
        return Image.fromarray(persp)

    img = get_block(equiRect, 90, deg_x,0)
    img.save(outname,"PNG")
    
import sys
import os
    
def main(deg_x):
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <indir> <outdir>")
        sys.exit(1)

    indir = sys.argv[1]
    outdir = sys.argv[2]

    if not os.path.exists(indir):
        print("Error: Input directory does not exist")
        sys.exit(1)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for filename in os.listdir(indir):
        infile = os.path.join(indir, filename)
        if os.path.isfile(infile):
            base, extension = os.path.splitext(filename)
            outname = base +"_" +str(deg_x) + extension
            outpath = os.path.join(outdir, outname)
            convert(infile, outpath,deg_x)

if __name__ == "__main__":
    main(-45)
