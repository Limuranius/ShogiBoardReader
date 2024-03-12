# ShogiBoardReader
Program that can recognize image/video of shogi board and convert it to digital formats (kifu, sfen) 

![shogi](https://github.com/Limuranius/ShogiBoardReader/assets/71573098/684ee640-cd8a-4a13-8150-7fd9b4c7d2aa)

### How to use
Download latest release of ShogiVision, install it and use it.

### About
ShogiVision uses Convolutional Neural Network to recognize figure and its direction inside every cell of shogi board. It can work with videos, images and pdf books. All you need to do is specify what it works with. 

There are four main components used by ShogiVision:
- Image source. Could be either photo, video or camera
- Corner detector. Thing that tries to find 4 corners of shogi board on image
- Inventory detector (optional). This component tries to find inventories of each player on image.
- Memorizer. This component only works with video and camera. It keeps track of the game and stores history of moves by comparing current frame of video/camera with previous ones.

More about each element [here](./Elements/README.md)

### Training
If you're not satisfied with current model you can train your own. To train model you must have a dataset stored in ```ShogiNeuralNetwork/datasets/dataset```. You can use dataset created by me [here](#resources) or build your own dataset. Simply run ```create_models.py``` and models will be saved to ```models``` folder. Then replace model stored in ```ShogiVision/_internal/models``` with new one.

### Using your own dataset
If you want to train model based on your own data:
1. Launch ```tools/create dataset/main.py```
2. Drag images into window and select true cell values for each image
3. New dataset will be created at ```ShogiNeuralNetwork/datasets/```.

### Resources
- [Model](https://drive.google.com/drive/folders/1QTWss5RQerwVI-kkQVF-ml3MvJ0GjDcT?usp=sharing)
- [Dataset](https://drive.google.com/drive/folders/1HrZ2PqalGUQhEsnZh24-DDBiXgweO7rn?usp=sharing)
- [Videos](https://drive.google.com/drive/folders/18i83vt4UiXAwscvO0VYH0MkUnKvQFGvb?usp=sharing)
- [Images](https://drive.google.com/drive/folders/1lKfzcnO9T8nDU2GhFhHPv1JOf7HEbrxP?usp=sharing)
