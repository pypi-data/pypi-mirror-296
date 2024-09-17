import warnings

import numpy as np
import itertools as it

import cv2

def apply_slicing(array: np.ndarray, slices: list):
    tiles = []
    for slc in slices:
        tiles.append(array[slc])
    return np.asarray(tiles)

def tile(array, bounds):
    '''
    Applies slicing to the array as specified by bounds
            Parameters:
                    array( array ): the original image
                    bounds ( array ): array of bounds returned by calculate_bounds
            Returns:
                    tiles ( array ): array of sliced images
    '''
    slices = bounds_to_slices(bounds)
    tiles = apply_slicing(array, slices)
    return tiles

def stitch(tiles, bounds, stitch_type='max'):
    '''
    Stitches the tiles together using the specified method, 
            Parameters:
                    tiles ([tiles]): tiles to stitch 
                    bounds ( array ): array of bounds returned by calculate_bounds
                    stitch_type (string): 'min', 'max' or 'multiband'
            Returns:
                    array ( image ): stitched image result
    '''
    slices = bounds_to_slices(bounds)
    if(stitch_type == 'min'):
        max = 0
        for tile in tiles:
            max = np.max(tile, initial = max) 
        full_mask = max*np.ones([np.max(bounds[:, i]) for i in range(bounds.shape[1])])
        for tile, slc in zip(tiles, slices):
            full_mask[slc] = np.minimum(full_mask[slc], tile) 
        return full_mask  
      
    if(stitch_type == 'max'):
        full_mask = np.zeros([np.max(bounds[:, i]) for i in range(bounds.shape[1])])
        for tile, slc in zip(tiles, slices):
            full_mask[slc] = np.maximum(full_mask[slc], tile) 
        return full_mask
    
    if(stitch_type == 'multiband'):
        fullImage = np.zeros([np.max(bounds[:, i]) for i in range(bounds.shape[1])])
        fullImageMask = np.zeros(fullImage.shape)
        newRowInImage = np.zeros(fullImage.shape)
        previousRowSlice = None
        firstRowPlaced = 0
        for i,r in it.groupby(bounds, lambda b: (b[0][0],b[0][1])):
            rows = list(r)
            offsetCorrectedRows = np.asarray(list(map(lambda x: np.asarray([[x[0][0]-x[0][0], x[0][1] -x[0][0] ], x[1], x[2]]), rows)))
            tiledRow = np.zeros([np.max(offsetCorrectedRows[:, i]) for i in range(offsetCorrectedRows.shape[1])])
            newTileRow = np.zeros(tiledRow.shape)

            maskRow = np.zeros([np.max(offsetCorrectedRows[:, i]) for i in range(offsetCorrectedRows.shape[1])])

            placedTileCounter = 0
            placedTileSlice = None
            placedTile = None
            for tile, tileSlice in zip(tiles, bounds_to_slices(offsetCorrectedRows)):
                if placedTileCounter == 0:
                    tiledRow[tileSlice] = tile
                    placedTile = tile
                else:
                    assert(newTileRow.shape[0] == tile.shape[0]) 
                    newTileRow[tileSlice] = tile
                    maskRow[placedTileSlice] = 1
                    
                    maskRow[(tileSlice[0],sliceOverlaps1D(tileSlice[1],placedTileSlice[1]),tileSlice[2])] = 0

                    max_leveln = int(np.floor(np.log2(min(tile.shape[0], tile.shape[1], placedTile.shape[0], placedTile.shape[1]))))
                    
                    MP = GaussianPyramid(maskRow, max_leveln)
                    LPA = LaplacianPyramid(tiledRow, max_leveln)
                    LPB = LaplacianPyramid(newTileRow, max_leveln)
                    blended = blend_pyramid(LPA, LPB, MP)
                    
                    # Reconstruction process
                    tiledRow = reconstruct(blended)
                    
                    newTileRow = np.zeros(tiledRow.shape)
                placedTileSlice = tileSlice
                placedTileCounter += 1 

            tiles = tiles[len(offsetCorrectedRows):]
            
            sliceToPlace = (slice(i[0],i[1]),slice(0,tiledRow.shape[1]),slice(0,tiledRow.shape[2]))

            if (firstRowPlaced == 0):
                fullImage[sliceToPlace] = tiledRow
                firstRowPlaced = 1
            else:
                assert(fullImage.shape[1] == tiledRow.shape[1]) 
                newRowInImage[sliceToPlace] = tiledRow
                fullImageMask[previousRowSlice] = 1
                fullImageMask[(sliceOverlaps1D(sliceToPlace[0],previousRowSlice[0]),sliceToPlace[1],sliceToPlace[2])] = 0
                
                max_leveln = int(np.floor(np.log2(min(tiledRow.shape[0], tiledRow.shape[1], fullImage.shape[0], fullImage.shape[1]))))

                MP = GaussianPyramid(fullImageMask, max_leveln)
                LPA = LaplacianPyramid(fullImage, max_leveln)
                LPB = LaplacianPyramid(newRowInImage, max_leveln)
                blended = blend_pyramid(LPA, LPB, MP)

                fullImage = reconstruct(blended)
                    
                newRowInImage[sliceToPlace] = 0
            previousRowSlice = sliceToPlace
        return fullImage
        
def sliceOverlaps1D(sliceA, sliceB):
    if (sliceA.start < sliceB.start):
        a=sliceA.start
        b=sliceA.stop
        c=sliceB.start
        d=sliceB.stop
    else :
        a=sliceB.start
        b=sliceB.stop
        c=sliceA.start
        d=sliceA.stop
    oEnd = oStart = c if (c<b) else None
    if oStart is not None :
        oEnd = d if (d<b) else b
    return slice(oStart+ int(np.floor(oEnd-oStart)/2) , oEnd  ) 

def GaussianPyramid(img, leveln):
    GP = [img]
    for i in range(leveln - 1):
        GP.append(cv2.pyrDown(GP[i]))
    return GP

def LaplacianPyramid(img, leveln):
    LP = []
    for i in range(leveln - 1):
        next_img = cv2.pyrDown(img)
        LP.append(img - cv2.pyrUp(next_img, dstsize = img.shape[1::-1])) # dstsize =
        img = next_img
    LP.append(img)
    return LP

def blend_pyramid(LPA, LPB, MP):
    blended = []
    for i, M in enumerate(MP):
        blended.append(LPA[i] * M + LPB[i] * (1.0 - M))
    return blended

def reconstruct(LS):
    img = LS[-1]
    for lev_img in LS[-2::-1]:
        img = cv2.pyrUp(img, dstsize = lev_img.shape[1::-1]) # dstsize =
        img += lev_img
    return img   

def calculate_bounds(
    full_shape, tile_shape, overlap, ignore_remainder=False
) -> np.ndarray:
    '''
    calculate_bounds(full_shape, tile_shape, overlap, ignore_remainder=False)
    For 'full_shape' computes tile bounds with 'tile_shape' sized tiles having an overlap specified by 'overlap'
            Parameters:
                    full_shape ([int]): full dimensions which should be sliced
                    tile_shape ([int]): tile sizes
                    overlap ([int]): overlap size
                    ignore_remainder (bool) : if set to true, remaining tile is ignored
            Returns:
                bounds (np.array) : bounds for tiling and stitching
            Example: 2x2 tiles heigth 10 width 20 tile size 6x14 overlap on heigth 2  and on width 6
                tile_stitch.calculate_bounds([10,20],[6,14],[2,6])
                array([[[0, 6],     ## first row
                        [0, 14]],   ## first column

                       [[0, 6],     ## first row
                        [6, 20]],   ## second column
 
                       [[4, 10],    ## second row
                        [0, 14]],   ## first column

                       [[4, 10],    ## second row
                        [6, 20]]], dtype=object) ## second column
    '''
    full_shape = np.asarray(full_shape)
    tile_shape = np.asarray(tile_shape)
    overlap = np.asarray(overlap)
    assert len(full_shape) == len(tile_shape) == len(overlap)

    tile_shape[tile_shape == None] = full_shape[tile_shape == None]
    assert np.all(tile_shape > 0)

    overlap[overlap == None] = 0
    assert np.all(overlap >= 0)

    if np.any(tile_shape > full_shape):
        warnings.warn(
            "Max tile shape should not be greater than full shape in any dimension!"
        )
        tile_shape[tile_shape > full_shape] = full_shape[tile_shape > full_shape]

    assert np.all(overlap < tile_shape)

    step_size = tile_shape - overlap
    remainder = (full_shape - overlap) % step_size != 0
    standard_steps = (full_shape - overlap) // step_size

    bounds = []

    for dimension, dimension_standard_steps in enumerate(standard_steps):
        
        dimension_bounds = []
        for i in range(dimension_standard_steps):
            dimension_bounds.append(
                np.array(
                    (
                        i * step_size[dimension],
                        overlap[dimension] + (i + 1) * step_size[dimension],
                    )
                )
            )
        if (not ignore_remainder) and remainder[dimension]:
            dimension_bounds.append(
                np.array(
                    (
                        np.array(full_shape[dimension] - tile_shape[dimension]),
                        np.array(full_shape[dimension]),
                    )
                )
            )
        bounds.append(np.array(dimension_bounds, dtype=object))
    return np.asarray(list(it.product(*bounds)))

def bounds_to_slices(bounds: np.ndarray) -> list:
    """
    Creates list of slices from array of bounds.
    Slices can be used for indexing n-dimensional array
    without knowing the number of dimensions.

    :arg bounds: Array of bounds for slicing n-dimensional array.
    Shape of bounds should be (chunks, each_chunk_ndim, 2).
    Last dimension is of size 2 as it contains (lower_bound, upper_bound).
    """
    assert len(bounds.shape) == 3
    assert bounds.shape[-1] == 2

    slices = list()
    for b in bounds:
        slices.append(
            tuple([slice(lower_bound, upper_bound) for lower_bound, upper_bound in b])
        )
    return slices
