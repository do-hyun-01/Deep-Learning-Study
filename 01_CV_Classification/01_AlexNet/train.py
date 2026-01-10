import torch
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        
        # 1. Feature Extractor (특징 추출부: Conv Layers)
        self.features = nn.Sequential(
            # Layer 1
            # 입력: 224x224x3 -> 출력: 55x55x64
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2), # Overlapping Pooling
            
            # Layer 2
            # 입력: 27x27x64 -> 출력: 27x27x192
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            
            # Layer 3
            # 입력: 13x13x192 -> 출력: 13x13x384
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            
            # Layer 4
            # 입력: 13x13x384 -> 출력: 13x13x256
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            
            # Layer 5
            # 입력: 13x13x256 -> 출력: 6x6x256
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        
        # 입력 이미지 크기에 상관없이 6x6 크기로 고정 (최신 PyTorch 구현 트렌드)
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        
        # 2. Classifier (분류부: Fully Connected Layers)
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5), # 핵심 기술: 과적합 방지
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            
            nn.Dropout(p=0.5), # 핵심 기술: 과적합 방지
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            
            nn.Linear(4096, num_classes), # 최종 출력: 1000개 클래스
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1) # 1차원으로 펼치기 (Batch size 제외)
        x = self.classifier(x)
        return x
