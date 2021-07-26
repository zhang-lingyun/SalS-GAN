# SalS-GAN
The code for our paper SalS-GAN: Spatially-Adaptive Latent Space in StyleGAN for Real Image Embedding. Our code is heavily borrowed from <a>https://github.com/genforce/idinvert</a>.

# Inversion Example
## Step-1:Get Pretrained Models
Download the pre-trained models(StyleGAN models and VGG model) and put them in ./models/pretrain. You can find ll the pretrained model in <a>https://github.com/genforce/idinvert</a>.
## Step-2:Invert Image
python invert.py styleganinv_tower256  tower_val_256x256/test.list -o ./outputs/tower  --num_iterations 3000

# Citation
@inproceedings{zhang2021salsgan,
  title={SalS-GAN: Spatially-Adaptive Latent Space in StyleGAN for Real Image Embedding},
  author={Lingyun Zhang, Xiuxiu Bai, and Yao Gao},
  booktitle={Proceedings of the 29th ACM International Conference on Multimedia (MM ’21)},
  year={2021}
}
