from torchvision import datasets, transforms

from dataset.BaseDataset import BaseDataset


class MNIST(BaseDataset):
    def __init__(self, clients, iid_config, params):
        BaseDataset.__init__(self, iid_config)
        transformer = transforms.Compose([
            # 将图片转化为Tensor格式
            transforms.ToTensor()
        ])
        # 获取数据集
        train_datasets = datasets.MNIST(root='../data/', train=True,
                                        transform=transformer, download=True)
        test_datasets = datasets.MNIST(root='../data/', train=False,
                                       transform=transformer, download=True)
        self.init(clients, train_datasets, test_datasets)
