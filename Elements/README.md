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
            <li>Hardcoded - uses predefined coordinates</li>
            <li>HSVThreshold - finds coordinates of markers that have certain color</li>
            <li>Cool - finds corners using edge detection</li>
        </ul>
    </td>    
</tr>
<tr>
    <td>FigureRecognizer</td>    
    <td>
        Receives image of board cell and tries to predict its figure and direction.
        Types of recognizers:
        <ul>
            <li>RecognizerNN - uses neural network to make predictions</li>
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
