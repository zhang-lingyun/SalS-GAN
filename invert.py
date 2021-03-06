# python 3.6
"""
invert a real image in our proposed sa latent space.
"""

import os
import argparse
from tqdm import tqdm
import numpy as np

from utils.inverter import StyleGANInverter
from utils.logger import setup_logger
from utils.visualizer import HtmlPageVisualizer
from utils.visualizer import save_image, load_image, resize_image


def parse_args():
  """Parses arguments."""
  parser = argparse.ArgumentParser()
  parser.add_argument('model_name', type=str, help='Name of the GAN model.')
  parser.add_argument('image_list', type=str,
                      help='List of images to invert.')
  parser.add_argument('-o', '--output_dir', type=str, default='',
                      help='Directory to save the results. If not specified, '
                           '`./results/inversion/${IMAGE_LIST}` '
                           'will be used by default.')
  parser.add_argument('--learning_rate', type=float, default=0.01,
                      help='Learning rate for optimization. (default: 0.01)')
  parser.add_argument('--num_iterations', type=int, default=3000,
                      help='Number of optimization iterations. (default: 3000)')
  parser.add_argument('--num_results', type=int, default=1,
                      help='Number of intermediate optimization results to '
                           'save for each sample. (default: 1)')
  parser.add_argument('--loss_weight_feat', type=float, default=5e-5,
                      help='The perceptual loss scale for optimization. '
                           '(default: 5e-5)')
  parser.add_argument('--loss_weight_enc', type=float, default=2.0,
                      help='The encoder loss scale for optimization.'
                           '(default: 2.0)')
  parser.add_argument('--viz_size', type=int, default=256,
                      help='Image size for visualization. (default: 256)')
  parser.add_argument('--gpu_id', type=str, default='0',
                      help='Which GPU(s) to use. (default: `0`)')
  parser.add_argument('--sizes', type=list, default=[(1,2,512,4,4),(1,2,512,4,4),(1,2,512,8,8),(1,2,512,8,8),(1,2,512,16,16),(1,2,512,16,16),(1,2,512,32,32),(1,2,512,32,32),(1,512),(1,512),(1,512),(1,512),(1,512),(1,512),],
                      help='sizes of the input latent code.')
  return parser.parse_args()


def main():
  """Main function."""
  args = parse_args()
  os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id
  assert os.path.exists(args.image_list)

  image_list_name = os.path.splitext(os.path.basename(args.image_list))[0]
  output_dir = args.output_dir or f'results/inversion/{image_list_name}'

  logger = setup_logger(output_dir, 'inversion.log', 'inversion_logger')
  logger.info(f'Loading model.')
  
  inverter = StyleGANInverter(
      args.model_name,
      learning_rate=args.learning_rate,
      iteration=args.num_iterations,
      reconstruction_loss_weight=1.0,
      perceptual_loss_weight=args.loss_weight_feat,
      regularization_loss_weight=args.loss_weight_enc,
      logger=logger)
  image_size = inverter.G.resolution

  # Load image list.
  logger.info(f'Loading image list.')
  image_list = []
  with open(args.image_list, 'r') as f:
    for line in f:
      image_list.append(line.strip())

  # Initialize visualizer.
  save_interval = args.num_iterations // args.num_results
  headers = ['Name', 'Original Image', 'Encoder Output']
  for step in range(1, args.num_iterations + 1):
    if step == args.num_iterations or step % save_interval == 0:
      headers.append(f'Step {step:06d}')
  viz_size = None if args.viz_size == 0 else args.viz_size
  visualizer = HtmlPageVisualizer(
      num_rows=len(image_list), num_cols=len(headers), viz_size=viz_size)
  visualizer.set_headers(headers)

  # Invert images.
  logger.info(f'Start inversion.')
  latent_codes = [ [] for _ in range(14)]

  for img_idx in tqdm(range(len(image_list)), leave=False):
    image_path = image_list[img_idx]
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = resize_image(load_image(image_path), (image_size, image_size))

    code, viz_results = inverter.easy_invert(image,args.sizes, num_viz=args.num_results)

    for idx,latent in enumerate(code):
      latent_codes[idx].append(code[idx].detach().cpu())

    save_image(f'{output_dir}/{image_name}_ori.png', image)
    save_image(f'{output_dir}/{image_name}_enc.png', viz_results[1])
    save_image(f'{output_dir}/{image_name}_inv.png', viz_results[-1])
    
    visualizer.set_cell(img_idx, 0, text=image_name)
    visualizer.set_cell(img_idx, 1, image=image)
    for viz_idx, viz_img in enumerate(viz_results[1:]):
      visualizer.set_cell(img_idx, viz_idx + 2, image=viz_img)

  # Save results.
  # for idx,latent_code in enumerate(latent_codes):
  #   np.save(f'{output_dir}/inverted_codes_%d.npy'%idx,np.concatenate(latent_code, axis=0))

  os.system(f'cp {args.image_list} {output_dir}/image_list.txt')
  visualizer.save(f'{output_dir}/inversion.html')


if __name__ == '__main__':
  main()
