this directory contains software scripts and docs for tasks that support the biologists in several experiments.


square size, marker size: 4cm, 5.5cm (oder 7mm)

https://cameradecision.com/faq/what-is-the-Sensor-Size-of-GoPro-Hero9-Black
https://gopro.github.io/labs/control/metadata/
https://ksimek.github.io/2013/08/13/intrinsic/

the formula seems to be:
$f_x = focal_length_{mm} \cdot \frac{pixel_{width}}{sensor_{width}_{mm}}$
$c_x = pixel_width / 2.0$
use crop width instead of pixel width if present everywhere. It seems that for crops on 360deg cameras nothing (especially not the principal point)
but if you shift the principal point c_x by the radial motion, the pose will stay the same. $c_x_s = c_x - 0.5pixel_width(theta/360) $ here pixel width is explicitly not the crop width!
