# tile_stitch

(this was a university submission project)

Package implements methods for image dissection into tiles and their recomposition with three different stitching method.

The three implemented methods at the moment:
- min
- max
- multiband

min and max behaves similarly, when there is an overlap a max or min function is applied to the overlapping area, this way each color channel is compared on a pixel level and a max or min value is used per channel for the final image. 

In multiband mode the module uses this implementation https://github.com/cynricfu/multi-band-blending 




## Blending example
![result](./exampleimages/ll.png) |  ![result](./exampleimages/rr.png)
:-------------------------:|:-------------------------:
image 1             | image 2

![result](./exampleimages/min.png) |  ![result](./exampleimages/max.png) | ![result](./exampleimages/multiband.png)
:-------------------------:|:-------------------------:|:-------------------------:
minimum              | maximum          | multiband

# Installing requirements
- python >= 3
- numpy==2.1.0
- opencv-python==4.10.0.84

```
python3 -m pip install numpy opencv-python
```

# Installing tile_stitch package
from PyPI repoisitory
```
python3 -m pip install tile_stitch
```
or from this git pulled repo (requires setuptools)
```
python3 setup.py sdist bdist_wheel
python3 -m pip install . 
```
# Usage example

As a module 
```
python3 -m tile_stitch -s exampleimages/ll.png -f exampleimages/rr.png -o 100 -m multiband -r result.png
```

or source code, excerpt from main
```py
import tile_stitch
import cv2

img1 = cv2.imread('img1.png')
img2 = cv2.imread('img2.png')

overlap_w = 20 #20px overlap
bounds = tile_stitch.calculate_bounds([img1.shape[0],img1.shape[1],img1.shape[2]],[int(img1.shape[0]/2)+overlap_w,int(img1.shape[1]/2)+overlap_w,img1.shape[2]],[overlap_w,overlap_w,0])

tiles1 = tile_stitch.tile(img1,bounds) # tiles from img1 
tiles2 = tile_stitch.tile(img2,bounds) # tiles from img2

tiles = [tiles1[0], tiles2[1], tiles2[2], tiles1[3]] # combined into one array

result = tile_stitch.stitch(tiles, bounds, stitch_type='multiband') 

cv2.imwrite('result', result)

```



