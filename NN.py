import torch
import torch.nn as nn
import torch.optim as optim
import PIL

import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.utils import save_image


class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()

        self.chosen_features = ['0', '5', '10', '19', '28']
        self.model = models.vgg19(pretrained=True).features[:29]

    def forward(self, x):
        features = []

        for layer_num, layer in enumerate(self.model):
            x = layer(x)

            if str(layer_num) in self.chosen_features:
                features.append(x)
        return features


def load_style_image(image_name, image_height, image_width):
    image = PIL.Image.open(image_name)
    loader = transforms.Compose(
        [
            transforms.Resize((image_height, image_width)),
            transforms.ToTensor(),
        ]
    )
    image = loader(image).unsqueeze(0)
    return image.to(device)


def load_original_image(image_name):
    image = PIL.Image.open(image_name)
    (image_width, image_height) = image.size
    loader = transforms.Compose(
        [
            transforms.Resize((image_height, image_width)),
            transforms.ToTensor(),
        ]
    )
    image = loader(image).unsqueeze(0)
    return image.to(device), image_height, image_width


device = torch.device('cpu' if torch.cuda.is_available else 'cpu')
# Now cuda doesn't work due to incompatibility between cuda and pytorch versions
# device = torch.device('cuda' if torch.cuda.is_available else 'cpu')


model = VGG().to(device).eval()
# generated = torch.randn(original_img.shape, device = device, requires_grad = True)


# hyperparameters
total_steps = 101
learning_rate = 0.05
alpha = 1
beta = 0.2
# optimizer = optim.Adam([generated], lr=learning_rate)


def make_image(original_img, style_img):
    original_img, image_height, image_width = load_original_image(original_img)
    style_img = load_style_image(style_img, image_height, image_width)
    generated = original_img.clone().requires_grad_(True)
    optimizer = optim.Adam([generated], lr=learning_rate)
    for step in range(total_steps):
        generated_features = model(generated)
        original_img_features = model(original_img)
        style_features = model(style_img)

        style_loss = original_loss = 0

        for gen_feature, orig_feature, style_feature in zip(
                generated_features, original_img_features, style_features
        ):
            batch_size, channel, height, width = gen_feature.shape
            original_loss += torch.mean((gen_feature - orig_feature) ** 2)

            # Gram Matrix
            G = gen_feature.view(channel, height * width).mm(
                gen_feature.view(channel, height * width).t()
            )

            A = style_feature.view(channel, height * width).mm(
                style_feature.view(channel, height * width).t()
            )

            style_loss += torch.mean((G - A) ** 2)

        total_loss = alpha * original_loss + beta * style_loss
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        if step % 5 == 0:
            print(f'Now step number: {step}')

        if step == 30:
            # print(total_loss)
            print(f'Now step number: {step}')
            picturename = 'generated1.png'
            save_image(generated, picturename)
            return picturename
            # files.download("generated.png")
