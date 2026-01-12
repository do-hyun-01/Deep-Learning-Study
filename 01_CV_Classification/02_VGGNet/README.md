## **논문 정보**

- **제목:** Very Deep Convolutional Networks for Large-Scale Image Recognition
- **저자:** Karen Simonyan, Andrew Zisserman (VGG: Visual Geometry Group, Oxford Univ.)
- **발표:** ICLR 2015

> https://arxiv.org/abs/1409.1556
> 

### **1. 서론 (Introduction)**

- **배경:** 2012년 AlexNet 이후 CNN의 성능을 높이기 위한 다양한 시도가 있었음.
- **문제점:** 기존 모델들(AlexNet, ZFNet)은 첫 레이어에 $11 \times 11$이나 $7 \times 7$ 같은 큰 필터를 사용했고, 하이퍼파라미터 튜닝에 의존적이었음. "네트워크의 깊이(Depth)가 성능에 얼마나 결정적인 영향을 미치는가?"에 대한 명확한 기준이 부족했음.
- **목표:** '깊이(Depth)'를 핵심 요소로 보고, 가장 작은 필터($3 \times 3$)만을 사용하여 네트워크를 매우 깊게 쌓았을 때의 성능 향상을 입증.

### **2. 전체 구조 (Architecture)**

- **모델 개요:** 16개(VGG16) 또는 19개(VGG19)의 Weight Layer (Conv + FC). AlexNet(8개)보다 훨씬 깊어짐.
- **입력:** $224 \times 224 \times 3$ 이미지 (RGB 평균값만 뺀 전처리)
- **출력:** 1000-way Softmax
- **특이점:** 구조의 단순화 (Simplicity)
    - 모든 Conv Layer에 $3 \times 3$ 필터, Stride $1$, Padding $1$ 적용.
    - Pooling은 $2 \times 2$ Max Pooling (Stride $2$) 사용.
    - 복잡한 변화 없이 채널 수만 2배씩 늘려가는($64 \to 128 \to 256 \to 512$) 규칙적인 구조.

### **3. 핵심 기술 1: 3x3 Convolution의 활용 (Factorization)**

- **기존 방식:** AlexNet은 $11 \times 11$, ZFNet은 $7 \times 7$ 등 큰 커널을 사용하여 한 번에 넓은 영역(Receptive Field)을 보려 했음.
- **VGGNet의 선택:** 큰 필터 1개를 작은 필터 여러 개로 쪼개서 사용.
    - $3 \times 3$ Conv 2개를 쌓으면 $\approx$ $5 \times 5$ Conv 1개와 동일한 Receptive Field.
    - $3 \times 3$ Conv 3개를 쌓으면 $\approx$ $7 \times 7$ Conv 1개와 동일한 Receptive Field.
- **이점:**
    1. **비선형성(Non-linearity) 증가:** 레이어를 여러 번 거치면서 ReLU가 더 많이 포함되어, 모델이 더 복잡한 특징을 잘 학습함.
    2. **파라미터 수 감소:**
        1. $7 \times 7$ 1개: $49C^2$ 파라미터
        2.  $3 \times 3$ 3개: $3 \times (9C^2) = 27C^2$ 파라미터
        3. 결과적으로 **더 깊으면서도 파라미터 효율이 좋음.**
