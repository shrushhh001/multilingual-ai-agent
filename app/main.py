
import json

from app.graph.workflow import run_video_workflow


def main():

    print("\n========================================")
    print("     MULTILINGUAL AI VIDEO GENERATOR")
    print("========================================\n")

    # Get user prompt
    user_input = input("Enter user input: ").strip()

    if not user_input:
        print("Error: Please enter a video prompt.")
        return

    # Get expected narration language
    target_language = input("Enter narration language: ").strip()

    if not target_language:
        print("Error: Please enter a narration language.")
        return

    print("\nStarting video generation workflow...")

    try:
        result = run_video_workflow(
            user_input=user_input,
            target_language=target_language
        )

        # Prepare final JSON
        final_json = json.dumps(
            result["final_output"],
            indent=2,
            ensure_ascii=False
        )

        # Save output using UTF-8 encoding
        output_file = "final_output.json"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(final_json)

        print("\n========== FINAL VIDEO SCRIPT ==========")
        print("\nFinal output saved to:", output_file)

        print("\n========== JSON OUTPUT ==========\n")
        print(final_json)

    except Exception as e:
        print(f"\nError during video generation: {e}")


if __name__ == "__main__":
    main()
