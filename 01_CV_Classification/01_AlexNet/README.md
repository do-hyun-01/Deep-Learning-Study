# **논문 정보**

- **제목:** ImageNet Classification with Deep Convolutional Neural Networks
- **저자:** Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton
- **발표:** NIPS (현 NeurIPS) 2012

> https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
> 

### 1. 서론 (Introduction)

- **배경:** 2012년, 컴퓨터 비전 대회(ILSVRC)
- **문제점:** 기존 머신러닝(SVM 등)은 사람이 직접 특징을 설계해야 했음. ex) SIFT, HOG > 성능 향상의 한계
- **목표:** 대규모 데이터(ImageNet, 1000개 클래스)를 학습할 수 있는 깊고 강력한 신경망(CNN) 구현

### **2. 전체 구조 (Architecture)**

- **모델 개요:** 8개의 레이어 (5 Conv Layers + 3 Fully Connected Layers)
- **입력:**  224*224*3 이미지
- **출력:** 1000-way Softmax (1000개 클래스 확률)
- **특이점:** 두 갈래로 나뉜 구조 (Two GPUs)

![위아래 두 갈래로 나뉘어 있는 구조. 이는 당시 GPU(GTX 580) 메모리가 3GB밖에 안 돼서, 모델을 반으로 쪼개 두 대의 GPU에 나눠 담았기 때문임.](attachment:90ab3c51-0304-437e-8f53-2f3e1ca4513a:image.png)

위아래 두 갈래로 나뉘어 있는 구조. 이는 당시 GPU(GTX 580) 메모리가 3GB밖에 안 돼서, 모델을 반으로 쪼개 두 대의 GPU에 나눠 담았기 때문임.

### **3. 핵심 기술 1: ReLU Nonlinearity**

- **기존 방식:** Tanh 또는 Sigmoid $(f(x) = tanh(x))$
    ◦ 문제점: 양 끝단에서 기울기가 사라짐(Saturating), 학습 속도 느림
- **AlexNet의 선택:** **ReLU $(f(x) = max(0, x))$**
    ◦ 장점: Non-saturating nonlinearity. 기울기 소실 문제 해결
- **결과:** Tanh 대비 학습 속도 **6배** 향상

### **4. 핵심 기술 2: Overfitting 방지 전략**

- 파라미터가 6천만 개나 되기 때문에 과적합(Overfitting) 방지가 필수적
- **Dropout (드롭아웃):**
    ◦ Fully Connected Layer에서 뉴런을 50% 확률로 0으로 만듦
    ◦ 특정 뉴런에 의존하는 현상(Co-adaptation) 방지
- **Data Augmentation (데이터 증강):**
    ◦ **Patch & Reflection:** $256 \times 256$ 이미지를 $224 \times 224$로 무작위 크롭(Crop) 및 좌우 반전 (데이터 양 2048배 증가 효과)
    ◦ **PCA Color Augmentation:** RGB 픽셀 값의 주성분을 분석해 조명 강도와 색상을 변형

### **5. 기타 기술적 디테일 (Technical Details)**

- **Local Response Normalization (LRN):**
    ◦ 신경생물학의 '측억제(Lateral Inhibition)' 모방. 강한 신호가 주변 약한 신호를 억제
    ◦ (참고: 현재는 Batch Normalization이 더 좋아 잘 안 씀)
- **Overlapping Pooling:**
    ◦ Stride($s=2$)를 커널 크기($z=3$)보다 작게 설정
    ◦ 정보 손실을 줄이고 과적합을 약간 방지

### 6. 실험 결과 및 결론 (Results & Conclusion)

- **성능:** ILSVRC 2012 우승. Top-5 Error **15.3%** (2등은 26.2%)
- **의의:**
    1. **Feature Learning:** 사람이 특징을 짜는 시대에서, 모델이 특징을 배우는 시대로 전환
    2. **CNN의 부활:** 대규모 데이터 + GPU + CNN의 조합이 정답임을 증명

### 7. 질문 (Study Question)

1. **Q: 왜 논문에는 입력이 224인데 코드 구현체들은 227을 쓰나요?**
    - A: 논문에는 $224 \times 224$라고 적혀있지만, 패딩(Padding) 처리에 대한 설명이 부족했습니다. 실제 PyTorch 등의 구현체나 후속 연구를 보면 $227 \times 227$ (혹은 패딩을 포함한 계산)로 해야 수식이 딱 맞아떨어지는 경우가 많습니다. (AlexNet의 첫 Conv layer stride가 4이기 때문).
2. **Q: 왜 요즘은 LRN을 안 쓰나요?**
    - A: LRN은 복잡도 대비 성능 향상 폭이 미미하고 연산량이 많습니다. 나중에 나온 **Batch Normalization**이 학습 안정화와 성능 향상에 훨씬 탁월해서 대체되었습니다.
3. **Q: 활성화 함수로 왜 ReLU를 썼나요?**
    - A: Gradient Vanishing(기울기 소실) 문제를 해결하고 연산 속도가 매우 빠르기 때문입니다.
4. Q: LRN은 언제까지 쓰였나요?
    - A: 2012년에 등장해서 약 2~3년 정도 짧게 쓰이다가, 2014~2015년 기점으로 사실상 사라졌습니다.
