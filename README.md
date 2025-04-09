# 🔍 OCR 기반 개인정보 탐지 도구

## 📖 소개
Tesseract OCR을 활용해 이미지 내에서 **개인정보를 자동 탐지**하는 Python 기반 도구입니다. 이메일, 전화번호, 이름, 계좌번호, 주민등록번호, 사업자등록번호 등 다양한 개인정보 유형을 탐지하고 해당 텍스트의 좌표를 함께 제공합니다.

---

## 🧠 주요 기능

- 이미지 내 텍스트 인식 (OCR)
- 15가지 개인정보 유형 정규표현식 패턴 기반 탐지
- 각 탐지된 항목의 텍스트, 좌표, 크기 출력

## 📦 설치 방법

1. **Tesseract OCR 설치**  
   [Tesseract 공식 설치 링크](https://github.com/tesseract-ocr/tesseract)

2. **Python 패키지 설치**
   
```pip install pytesseract pillow```


 ## 📂 이미지 예시 파일 구조
```
project/
│
├── image/
│   ├── example1.jpg
│   └── example2.png
│
├── ocr_scan.py
└── README.md
```

  ## 🔎 탐지 가능한 개인정보 유형


| 항목 | 설명 예시 |
|------|-----------|
| 이메일 주소 (Email address) | example@domain.com |
| 이름 (Names) | 홍길동, 김철수 |
| 전화번호 (Phone numbers) | 010-1234-5678, 02-123-4567 |
| 주민등록번호 (RRN) | 900101-1234567 |
| 고유 식별자 (Unique ID) | USR-123456, EMP-654321 |
| 신용카드 번호 (Credit Card) | 1234-5678-1234-5678 |
| 계좌번호 (Bank Account) | 110-123-456789 |
| 금액 정보 (Money) | ₩1,000, 10,000.00 |
| 사업자등록번호 (Business Reg) | 123-45-67890 |
| 세금 관련 번호 (Taxpayer) | 123-45-678901 |
| 웹사이트 주소 (URLs) | https://example.com |
| IP 주소 (IP Address) | 192.168.0.1 |
| MAC 주소 (MAC Address) | 00:1A:2B:3C:4D:5E |
| 차량 번호판 (License Plate) | 서울12가 1234 |
| 커스텀 필터 (Custom) | 내부문서-2024, 보안등급: 기밀 |

