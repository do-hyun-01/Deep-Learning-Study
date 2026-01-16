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

### **4. 핵심 기술 2: Fully Convolutional Network 관점과 1x1 Conv**

- **1x1 Convolution:**
    - Network in Network(NIN) 논문의 개념 차용.
    - Receptive Field에는 영향을 주지 않으면서 비선형성(ReLU)을 추가하고 채널 수를 조절하는 역할.
- **Dense to Conv (테스트 시):**
    - 학습된 FC(Fully Connected) Layer를 $1 \times 1$ Conv Layer로 변환하여 사용 가능.
    - 이렇게 하면 입력 이미지 크기가 $224 \times 224$로 고정되지 않아도 되며, 이미지를 자르지(Crop) 않고 전체를 입력으로 넣는 **Sliding Window** 방식 적용이 가능해짐.
    ****

### **5. 기타 기술적 디테일 (Technical Details)**

- **LRN 제거:** AlexNet에서 썼던 Local Response Normalization(LRN)이 성능 향상에 도움이 되지 않고 메모리만 차지한다고 판단하여 제거.
- **Multi-scale Training (Scale Jittering):**
    - 학습 시 이미지의 짧은 변(S)을 256에서 512 사이의 값으로 무작위 조절(Resizing)한 후 $224 \times 224$로 크롭.
    - 다양한 크기의 객체를 인식하도록 학습하는 데이터 증강 기법.
- **초기화 전략:** 깊은 망은 학습이 어려우므로, 얕은 구조(11 layer)를 먼저 학습시킨 가중치로 깊은 구조를 초기화함 (후에는 Xavier 초기화로 해결).

### **6. 실험 결과 및 결론 (Results & Conclusion)**

- **성능:** ILSVRC 2014 준우승 (Classification). Top-5 Error **7.3%**.
    - (참고: 우승은 GoogleNet이었으나, 구조가 복잡하여 실제 현업에서는 구조가 단순한 VGGNet이 더 많이 쓰임)
- **의의:**
    - **"Deeper is Better"**: 깊이가 깊어질수록 성능이 좋아짐을 명확히 증명.
    - **Backbone의 표준**: $3 \times 3$ Conv를 블록으로 쌓는 단순하고 규칙적인 구조는 이후 ResNet 등 현대 CNN 아키텍처의 표준 디자인 패턴이 됨.

### **7. 질문 (Study Question)**

- **Q: 왜 짝수 크기(**$2 \times 2, 4 \times 4$**) 필터가 아닌** $3 \times 3$ **홀수 필터를 쓰나요?**
    - **A:** 홀수 필터를 써야 픽셀의 중심(Center pixel)이 명확해져서 패딩(Padding)을 통해 입력과 출력 크기를 동일하게 유지하기 쉽습니다. 또한 대칭적인 특징 추출에 유리합니다.
    
- **Q: VGGNet의 단점은 무엇인가요?**
    - **A:** 파라미터 수가 너무 많고 연산량이 큽니다. 특히 마지막 3개의 FC Layer에서만 약 1억 2천만 개의 파라미터가 발생하여 모델 용량(약 500MB 이상)이 매우 큽니다. (AlexNet의 3배 수준)
- **Q:** $1 \times 1$ **Convolution은 왜 쓰나요?**
    - **A:** 채널(차원) 수를 줄여 연산량을 감소시키거나, 차원을 유지하면서 비선형 활성화 함수(ReLU)를 추가하여 모델의 표현력을 높이기 위해 사용합니다. VGG에서는 주로 비선형성 증가 목적으로 언급됩니다.
- **Q: GoogleNet이 1등인데 왜 VGGNet이 더 유명한가요?**
    - **A:** GoogleNet(Inception 모듈)은 구조가 복잡하여 구현과 커스터마이징이 어렵습니다. 반면 VGGNet은 "3x3 Conv 반복"이라는 매우 단순한 구조 덕분에 이해하기 쉽고, 전이 학습(Transfer Learning)을 위한 Feature Extractor로 가져다 쓰기가 훨씬 편했기 때문입니다.
