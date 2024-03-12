# Elements

There are several main modules used by ShogiBoardReader


<table>
<tr>
    <td>ImageGetter</td>    
    <td>
        Returns image received from different sources, such as:
        <ul>
            <li>Photo</li>
            <li>Video</li>
            <li>Camera</li>
        </ul>
    </td>    
</tr>
<tr>
    <td>CornerDetector</td>    
    <td>
        Receives image of board and finds coordinates of its corners. Used types of detectors:
        <ul>
            <li>Hardcoded - uses manually defined coordinates</li>
            <li>HSVThreshold - finds coordinates of markers that have certain color using HSV thresholding</li>
            <li>Cool - finds corners using edge detection</li>
            <li>Book - also uses edge detection, faster than CoolCornerDetector but only works with e-books</li>
        </ul>
    </td>    
</tr>
<tr>
    <td>InventoryDetector</td>    
    <td>
        Receives image of board, finds coordinates of corners of each player's inventory and also image of each figure in inventory
        <ul>
            <li>Book - finds inventory in e-book board assuming that it is always located some pixels to left and right of the board</li>
        </ul>
    </td>    
</tr>
<tr>
    <td>Recognizer</td>    
    <td>
        Receives image of board cell and tries to predict its figure and direction using different algorithms.
        Types of recognizers:
        <ul>
            <li>RecognizerTF - uses Keras/Tensorflow model to make predictions</li>
            <li>RecognizerONNX - uses ONNX model to make predictions</li>
            <li>RecognizerFM - uses computer vision feature matching (removed due to very slow speed)</li>
        </ul>
    </td>    
</tr>
<tr>
    <td>BoardSplitter</td>
    <td>
        Combination of ImageGetter and CornerDetector. 
        Receives image using ImageGetter, finds corners using CornerDetector,
        removes perspective, crops board from image and splits it in 81 cells
    </td>
</tr>
<tr>
    <td>BoardMemorizer</td>
    <td>
        Keeps history of moves. Receives recognized board cells, 
        validates board state using previously accumulated boards
        and stores it in memory if validation is successful
    </td>
</tr>
</table>
