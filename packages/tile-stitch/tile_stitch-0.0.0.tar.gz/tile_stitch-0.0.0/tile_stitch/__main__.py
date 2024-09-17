import tile_stitch

import cv2
import argparse

ap = argparse.ArgumentParser( description="A Python implementation of multi-band blending")

ap.add_argument('-f', '--first', required=True,
                    help="path to the first image")
ap.add_argument('-s', '--second', required=True,
                    help="path to the second (right) image")
ap.add_argument('-o', '--overlap', required=True, type=int,
                    help="width of the overlapped area between two images")
ap.add_argument('-m', '--method', required=True, choices=['min', 'max', 'multiband'],
                    help="stitching method")
ap.add_argument('-r', '--result', default='./result.png',
                    help="result image path and filename")
args = vars(ap.parse_args())


img1 = cv2.imread(args['first'])
img2 = cv2.imread(args['second'])

overlap_w = args['overlap']
    
assert(img1.shape[0] == img2.shape[0])
assert(img1.shape[1] == img2.shape[1])
assert(img1.shape[2] == img2.shape[2])
assert(int(img1.shape[0]/2) > overlap_w)
assert(int(img1.shape[1]/2) > overlap_w)

bounds = tile_stitch.calculate_bounds([img1.shape[0],img1.shape[1],img1.shape[2]],[int(img1.shape[0]/2)+overlap_w,int(img1.shape[1]/2)+overlap_w,img1.shape[2]],[overlap_w,overlap_w,0])

tiles1 = tile_stitch.tile(img1,bounds)
tiles2 = tile_stitch.tile(img2,bounds)   
tiles = []
#for i in range(len(tiles1)):
#    if (i%2==0):
#        tiles.append(tiles1[i])
#    else:
#        tiles.append(tiles2[i])
tiles = [tiles1[0], tiles2[1], tiles2[2], tiles1[3]]

result = tile_stitch.stitch(tiles, bounds, stitch_type=args['method'])

cv2.imwrite(args['result'], result)
