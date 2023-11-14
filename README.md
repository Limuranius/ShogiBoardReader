# ShogiBoardReader
Program that can recognize image/video of shogi board and convert it to digital format (kifu) 

[VUMcIREdjc](https://github.com/Limuranius/ShogiBoardReader/assets/71573098/8d53cb61-6e27-4e45-9816-40d80cc4ee1c)

## How to use
### Requirements
- Python 3.10
- Tensorflow with GPU support (could work on CPU, but training would take ages to complete)
### Installation
```pip install -r requirements.txt```

### Training
To train models run ```create_models.py```. 
Models will be saved to ```models``` folder 

### Using your own dataset
If you want to train model based on your own data:
1. Load your images of boards to ```img/boards```
2. Write info about each loaded picture to ```ShogiNeuralNetwork/true_boards.txt```. 
Info must include coordinates of each corner, labeled figures types and labeled figures directions.
3. Add path of each image to list ```IMGS``` in ```ShogiNeuralNetwork/data_info.py```.
Path must be relative to folder ```img/boards```

WARNING: alarm that memorizer fires when it can't recognize board is VERY loud so make sure your sound is as low as possible before running app with board memorizer.