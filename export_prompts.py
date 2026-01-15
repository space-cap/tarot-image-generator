import json
import os

OUTPUT_FILE = "docs/TAROT_PROMPTS_LIST.md"
INPUT_FILE = "tarot_prompts.json"

COMMON_STYLE = (
    "Tarot card design, mystical, spiritual, heavily detailed, 8k resolution, "
    "art nouveau style, masterpiece, vibrant colors, golden ratio, "
    "full card illustration, sharp focus, intricate patterns"
)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🔮 Full Tarot Card Prompts List (78 Cards)\n\n")
        f.write("이 문서는 타로 카드 78장의 전체 프롬프트 리스트입니다. 복사해서 이미지 생성 AI(Midjourney, ChatGPT 등)에 사용하세요.\n\n")
        f.write(f"**공통 스타일(Common Style):**\n> {COMMON_STYLE}\n\n")
        f.write("---\n\n")

        # 1. Major Arcana
        f.write("## 1. Major Arcana (22 Cards)\n\n")
        for card_id, desc in data['major_arcana'].items():
            full_prompt = f"{COMMON_STYLE}, {desc}"
            f.write(f"### {card_id}. {desc.split(':')[0]}\n") # Title from description
            f.write("```text\n")
            f.write(full_prompt)
            f.write("\n```\n\n")

        # 2. Minor Arcana
        f.write("## 2. Minor Arcana (56 Cards)\n\n")
        suits = data['minor_arcana']['suits']
        ranks = data['minor_arcana']['ranks']

        for suit, suit_desc in suits.items():
            f.write(f"### Suit of {suit}\n\n")
            for rank, rank_desc in ranks.items():
                specific_prompt = f"{suit} suit card, {rank}, {suit_desc}, {rank_desc}"
                full_prompt = f"{COMMON_STYLE}, {specific_prompt}"
                
                f.write(f"#### {rank} of {suit}\n")
                f.write("```text\n")
                f.write(full_prompt)
                f.write("\n```\n")
            f.write("\n---\n\n")

    print(f"✅ Successfully created {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
