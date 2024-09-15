# NovaNet


NovaNet: An advanced convolutional neural network architecture derived from the traditional U-Net framework, specifically designed to address complex image segmentation tasks. NovaNet enhances the basic U-Net by incorporating several innovative features aimed at improving both accuracy and contextual awareness. Key enhancements include:

* Multi-Scale Feature Fusion: NovaNet intelligently combines features from various network depths before the final output, ensuring that both fine details and broader semantic contexts are captured effectively. This approach allows the network to make more informed predictions, especially beneficial in tasks requiring precise localization and delineation of intricate structures.
* CoordConv Layers: By integrating CoordConv layers, NovaNet gains an innate spatial awareness, allowing it to better understand and process the positional aspects of input data. This is particularly useful in segmentation tasks where the position and layout of the objects are crucial.
* Gated Convolutional Layers: These layers enable dynamic feature selection during the learning process. By applying gates to the convolutions, NovaNet can selectively emphasize or de-emphasize certain features based on their relevance to the task, leading to more robust and adaptable feature representations.
* Attention Gates: These gates are strategically placed within the network to focus the model’s capacity on salient parts of the input image, thereby improving the quality of feature extraction and subsequent segmentation performance.
* Adaptive Dilation and SE Blocks: NovaNet uses adaptive dilation rates to adjust its receptive field based on the scale of features in the input, complemented by Squeeze-and-Excitation (SE) blocks that recalibrate channel-wise feature responses to boost the representational power of the network.
NovaNet is designed to be highly flexible and efficient, suitable for a wide range of segmentation tasks, including but not limited to medical imaging, satellite image analysis, and scene parsing. Its architecture supports extensive customization to meet specific performance criteria and adapt to various types of image data.

## Architecture

The NovaNet architecture includes clever use of gated convolution operations making it a better performer than UNet++ in terms of performance and architecture simplicity.
![plot](./images/NovaNet.png)

## Results

![plot](./images/samples_1.png)

![plot](./images/samples_2.png)
