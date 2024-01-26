# Documentation for the function eucli_intersection_2p in src/datastruct/worksite

Function to calculate the Euclidean coordinates of a point, visible on two acquisitions. Function built in worksite to calculate from 2 acquisitions.

## Parameters

1. name_copoint: the name of the link point you wish to calculate its field position, in str format.
2. shot1: first acquisition where the point is visible and its image coordinates are known, Shot object format.
3. shot2: second acquisition where the point is visible and its image coordinates are known, Shot object format.

The Shot object is an object for an acquisition that defines it, with a name, position, rotation angles and camera name.

## Calculation step

### Data recovery

```
# Recover point position in images
p_img1 = shot1.copoints[name_copoint]
p_img2 = shot2.copoints[name_copoint]

# Recover camera for each image
cam1 = self.cameras[shot1.name_cam]
cam2 = self.cameras[shot2.name_cam]
```

### Converting image data to Euclidean projection

* Conversion of acquisition positions in the Euclidean reference frame
```
pos_eucli1 = self.projeucli.world_to_euclidean(shot1.pos_shot[0],shot1.pos_shot[1],shot1.pos_shot[2])
pos_eucli2 = self.projeucli.world_to_euclidean(shot2.pos_shot[0],shot2.pos_shot[1],shot2.pos_shot[2])
```

* Calculates image-to-Euclidean reference frame change matrices for each shot
```
mat_eucli1 = self.projeucli.mat_to_mat_eucli(shot1.pos_shot[0],shot1.pos_shot[1],shot1.mat_rot).T
mat_eucli2 = self.projeucli.mat_to_mat_eucli(shot2.pos_shot[0],shot2.pos_shot[1],shot2.mat_rot).T
```

### Euclidean position calculation

* Base calculation
```
base = pos_eucli1 - pos_eucli2
```

* Calculates the vectors of each beam by acquisition
```
vect1 = mat_eucli1 @ np.array([p_img1[0] - cam1.ppax,
                               p_img1[1] - cam1.ppay,
                               -cam1.focal])
vect2 = mat_eucli2 @ np.array([p_img2[0] - cam2.ppax,
                               p_img2[1] - cam2.ppay,
                               -cam2.focal])
```

* Calculates products scalar product
```
norme_v1 = vect1 @ vect1
norme_v2 = vect2 @ vect2
v1_v2 = vect1 @ vect2
b_v1 = base @ vect1
b_v2 = base @ vect2
```

* Calculates the position of the point on the beam
```
p1_eucli = pos_eucli1 + ((b_v2*v1_v2 - b_v1*norme_v1)/(v1_v2**2 - norme_v1*norme_v2))*vect1
p2_eucli = pos_eucli2 + ((b_v2*norme_v1 - b_v1*v1_v2)/(v1_v2**2 - norme_v1*norme_v2))*vect2
```

* Return the average position between the two points
```
return 0.5 * (p1_eucli + p2_eucli)
```

##  Example to use
```
import numpy as np
from src.datastruct.worksite import Worksite

# Create worksite with just a name
work = Worksite("Test")

# Add two shots
work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
work.add_shot("shot2",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")

# Setup projection
work.set_proj("EPSG:2154", "test/data/proj.json", "./test/data/")

# Add camera information
work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)

# Add connecting points in each shot
work.add_copoint('"1003"',"shot1",24042.25,14781.17)
work.add_copoint('"1003"',"shot2",24120.2,10329.3)

# Calculate eucliean coordinate of intersection
coor = work.eucli_intersection_2p('"1003"', work.shots["shot1"], work.shots["shot2"])

# Transform euclidiean coordinate to world coordinate 
actual = work.projeucli.euclidean_to_world(coor[0], coor[1], coor[2])
```

![logo ign](../logo/logo_ign.png) ![logo fr](../logo/Republique_Francaise_Logo.png)