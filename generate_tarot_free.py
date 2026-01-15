import os
import time
import json
import requests
import random

# ---------------------------------------------------------
# 설정 (Configuration)
# ---------------------------------------------------------
OUTPUT_DIR = "assets/cards"
BASE_URL = "https://image.pollinations.ai/prompt"
MODEL = "flux"
WIDTH = 768
HEIGHT = 1024

COMMON_STYLE = (
    "Tarot card design, mystical, spiritual, heavily detailed, 8k resolution, "
    "art nouveau style, masterpiece, vibrant colors, golden ratio, "
    "full card illustration, sharp focus, intricate patterns"
)

# ---------------------------------------------------------
# 함수 정의
# ---------------------------------------------------------

def generate_image_pollinations(prompt, filename, max_retries=10):
    """
    Pollinations.ai를 통해 이미지를 다운로드합니다.
    Rate Limit 발생 시 대기 후 재시도합니다.
    """
    full_prompt = f"{COMMON_STYLE}, {prompt}"
    
    retry_count = 0
    while retry_count < max_retries:
        seed = random.randint(1, 999999)
        # URL에 시드와 모델 파라미터를 포함 (랜덤 시드로 매번 다르게)
        url = f"{BASE_URL}/{full_prompt}"
        params = {
            "width": WIDTH,
            "height": HEIGHT,
            "seed": seed,
            "model": MODEL,
            "nologo": "true"
        }

        print(f"Generating: {filename} (Attempt {retry_count + 1})...")
        
        try:
            response = requests.get(url, params=params, timeout=60)
            
            # 429 Error (Too Many Requests) 체크 -> 텍스트로 올 수도 있음
            if response.status_code == 429 or "rate limit" in response.text.lower():
                raise Exception("Rate limit reached")
                
            response.raise_for_status()
            
            # 바이너리 데이터 저장
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
                
            print(f"✅ Saved: {filepath}")
            return True

        except Exception as e:
            print(f"⚠️ Error generating {filename}: {e}")
            
            # 대기 시간: 기본 20초 + 시도 횟수 * 10초 (점점 늘어남)
            wait_time = 20 + (retry_count * 10)
            print(f"⏳ Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retry_count += 1

    print(f"❌ Failed to generate {filename} after {max_retries} retries.")
    return False

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        with open('tarot_prompts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: 'tarot_prompts.json' file not found.")
        return

    print(f"Starting generation using model: {MODEL}")
    
    # 1. 메이저 아르카나 생성
    print("\n--- Generating Major Arcana (22 cards) ---")
    for card_id, prompt_desc in data['major_arcana'].items():
        filename = f"major_{card_id}.png"
        
        # 파일이 이미 있으면 건너뛰기 (이어하기 기능)
        if os.path.exists(os.path.join(OUTPUT_DIR, filename)):
            print(f"⏭️ Skipping {filename} (Already exists)")
            continue

        success = generate_image_pollinations(prompt_desc, filename)
        if success:
            # 성공 후에도 랜덤 딜레이 (5~10초)를 줘서 서버 부하를 줄임
            sleep_time = random.uniform(5, 10)
            print(f"Checking next card in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

    # 2. 마이너 아르카나 생성
    print("\n--- Generating Minor Arcana (56 cards) ---")
    suits = data['minor_arcana']['suits']
    ranks = data['minor_arcana']['ranks']

    for suit, suit_desc in suits.items():
        for rank, rank_desc in ranks.items():
            prompt = f"{suit} suit card, {rank}, {suit_desc}, {rank_desc}"
            filename = f"minor_{suit}_{rank}.png"
            
            if os.path.exists(os.path.join(OUTPUT_DIR, filename)):
                print(f"⏭️ Skipping {filename} (Already exists)")
                continue

            success = generate_image_pollinations(prompt, filename)
            if success:
                sleep_time = random.uniform(5, 10)
                print(f"Checking next card in {sleep_time:.1f}s...")
                time.sleep(sleep_time)

    print("\n🎉 All processes finished!")

if __name__ == "__main__":
    main()
