from torchvision import datasets

from waterboy.api.base import Source

from waterboy.augmentations.normalize import Normalize
from waterboy.augmentations.to_tensor import ToTensor
from waterboy.augmentations.to_array import ToArray


def create(batch_size, model_config, normalize=True, num_workers=0, augmentations=None):
    """
    Create a CIFAR10 dataset, normalized.
    Augmentations are the same as in the literature benchmarking CIFAR performance.
    """
    path = model_config.data_dir('cifar10')

    train_dataset = datasets.CIFAR10(path, train=True, download=True)
    test_dataset = datasets.CIFAR10(path, train=False, download=True)

    augmentations = [ToArray()] + (augmentations[:] or [])
    
    if normalize:
        train_data = train_dataset.train_data
        mean_value = (train_data / 255).mean(axis=(0, 1, 2))
        std_value = (train_data / 255).std(axis=(0, 1, 2))

        augmentations.append(Normalize(mean=mean_value, std=std_value, tags=['train', 'val']))

    augmentations.append(ToTensor())

    return Source(
        train_dataset,
        test_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        augmentations=augmentations
    )
