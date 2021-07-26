# SalS-GAN
The code for our paper SalS-GAN: Spatially-Adaptive Latent Space in StyleGAN for Real Image Embedding.  
Our code is heavily borrowed from [Idinvert](https://github.com/genforce/idinvert).  
Feel free to raise any issues, we will reply to them as soon as possible.

# Inversion Example
## Step-1:Get Pretrained Models
Download pre-trained models(StyleGAN models and VGG model) and put them in "./models/pretrain". 
You can find some pretrained models in [Idinvert](https://github.com/genforce/idinvert).

## Step-2:Invert Image
python invert.py $MODEL_NAME $IMAGE_LIST -o $OUTPUT_DIR --num_iterations ITERATIONS  
example: python invert.py styleganinv_tower256  tower_val_256x256/test.list -o ./outputs/tower  --num_iterations 3000

# Citation
@inproceedings{zhang2021salsgan,  
  title={SalS-GAN: Spatially-Adaptive Latent Space in StyleGAN for Real Image Embedding},  
  author={Lingyun Zhang, Xiuxiu Bai, and Yao Gao},  
  booktitle={Proceedings of the 29th ACM International Conference on Multimedia (MM ’21)},  
  year={2021}  
}
