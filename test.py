import basic_intelligence
import utils

def run_tests():
    query = "What is the capital of France?"

    print("\n--- Test: Standard Completion Call ---")
    result = basic_intelligence.llm_call_blob(query)
    print(f"Result: {result}")

    print("\n--- Test: Streaming Completion Call ---")
    stream_result = basic_intelligence.llm_call_stream(query)
    print(f"\nStream Result: {stream_result}")

    print("\n--- Exporting logs to CSV ---")
    utils.convert_jsonl_to_csv()

if __name__ == "__main__":
    run_tests()
