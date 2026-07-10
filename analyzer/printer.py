def print_analysis(result):

    print("\n" + "=" * 70)
    print("PAGE ANALYSIS")
    print("=" * 70)

    for page in result:

        print(
            f"Page {page['page']:2d} | "
            f"{page['type']:9s} | "
            f"Text={page['text_length']:5d} | "
            f"Images={page['image_count']}"
        )

    print("=" * 70)