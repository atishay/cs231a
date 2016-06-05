Automatic 3D Reconstruction for Symmetric Shapes
------------------------------------------------

Steps to use:
* Install dependencies:
    * pip install vpython
    * pip install scipy
    * pip install numpy
    * Install opencv2 from the repo
 * Run the commands to try out
    ```Python
    python main.py <image name> <shape> <number of time to repeat texture>
    ```
 * Try using mouse right click to middle click to navigate in 3D
 * Shapes in the paper:
 ```
    python main.py coke.jpg
    python main.py ben.jpg square
    python main.py vase.jpg circle 2
    python main.py vase2.jpg circle 2
    python main.py can.png circle 2
    python main.py curved.jpg circle 2
    python main.py bottle.jpg circle 2
    python main.py bottle2.jpg circle 2
    python main.py pisa.jpg circle 2
    python main.py coke.jpg custom1
    python main.py coke.jpg custom2
    python main.py coke.jpg triangle 3
    python main.py wine.jpg circle 2

 ```
 * Mask output is availabe at mask.jpg
 * Texture map is available as temp.jpg
 * You can add new shapes in Object.py line no 12

--
Atishay Jain
CS231A 2016
atishay@stanford.edu
