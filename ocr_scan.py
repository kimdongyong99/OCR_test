import pytesseract
from PIL import Image
import re
import os

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 정규 표현식 패턴 모음
PATTERNS = {
    "이메일 주소": r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    "이름": r'[가-힣]{2,4}\s?[가-힣]{1,4}',
    "전화번호": r'(?:010|011|016|017|018|019)-\d{3,4}-\d{4}|\b0\d{1,2}-\d{3,4}-\d{4}\b',
    "주민등록번호": r'\b\d{6}-\d{7}\b',
    "고유 식별자": r'\b(?:USR|EMP)-\d{4,6}\b',
    "신용카드 번호": r'\b(?:\d{4}[- ]?){3}\d{4}\b',
    "계좌번호": r'\b\d{2,3}-\d{3,4}-\d{4,6}\b',
    "금액 정보": r'₩?\d{1,3}(?:,\d{3})*(?:\.\d+)?',
    "사업자등록번호": r'\b\d{3}-\d{2}-\d{5}\b',
    "세금 관련 번호": r'\b\d{3}-\d{2}-\d{6,10}\b',
    "웹사이트 주소": r'https?://[a-zA-Z0-9./?=&_-]+',
    "IP 주소": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "MAC 주소": r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
    "차량 번호판": r'\b[가-힣]{1,2}\s?\d{1,4}\s?[가-힣]\s?\d{4}\b',
    "커스텀 필터": r'\b(?:내부문서-\d{4}|보안등급:\s?[가-힣]+)\b'
}

# 이미지 폴더 경로
IMAGE_FOLDER = "./image"


def extract_sensitive_data_from_image(image_path):
    """이미지에서 텍스트를 추출하고 개인정보 정규식 탐지"""
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    results = []

    for i, word in enumerate(data['text']):
        for label, pattern in PATTERNS.items():
            if re.search(pattern, word):
                x1, y1 = data['left'][i], data['top'][i]
                width, height = data['width'][i], data['height'][i]
                x2, y2 = x1 + width, y1 + height

                results.append({
                    "label": label,
                    "text": word,
                    "x1": x1, "y1": y1,
                    "x2": x2, "y2": y2,
                    "width": width,
                    "height": height
                })
    return results


def process_images_in_folder(folder_path):
    """폴더 내 이미지 파일들을 순회하며 OCR 및 패턴 매칭"""
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        print(f"❗ '{folder_path}' 폴더에 이미지 파일이 없습니다.")
        return

    for image_file in image_files:
        full_path = os.path.join(folder_path, image_file)
        results = extract_sensitive_data_from_image(full_path)

        print(f"\n📂 [파일]: {image_file}")
        if results:
            for r in results:
                print(
                    f"[{r['label']}] {r['text']} → 좌표: (x1={r['x1']}, y1={r['y1']}, x2={r['x2']}, y2={r['y2']}, w={r['width']}, h={r['height']})")
        else:
            print("🔍 탐지된 개인정보 없음.")


# 실행
if __name__ == "__main__":
    process_images_in_folder(IMAGE_FOLDER)
