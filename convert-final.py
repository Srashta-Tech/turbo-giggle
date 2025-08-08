from textractor.entities.document import Document

PAGE_NUMBER = 0
HEADER_LINES = 3

def remove_and_merge_bad_lines(page, kv_pairs, header_lines, page_number):
    bad_lines = []
    curr = 0
    # Exclude header and last line from processing
    for i, line in enumerate(page.lines[:-1]):
        if page_number == 0:
            if i < header_lines + 4:
                continue
        else:
            if i < header_lines:
                continue
        line_text = line.text.strip()
        for kv in kv_pairs:
            if line_text in kv.text:
                bad_lines.append(i + 1)
                kv_pairs.remove(kv)
                break

        if len(bad_lines) > curr and i == bad_lines[curr]:
            page.lines[i - 1]._children.extend(line._children)
            curr += 1

    bad_lines = sorted(bad_lines)
    if bad_lines and bad_lines[-1] >= len(page.lines):
        bad_lines.pop()
    while bad_lines:
        page.lines.pop(bad_lines.pop())

def pre_process_page(document, page_number=0, header_lines=3):
    page = document.page(page_number)
    kv_pairs = list(page.key_values)

    print("Raw lines:")
    for line in page.lines:
        print(line.text)
    print("\n\n----\n\n")

    # print("Key-Value Pairs:", kv_pairs)
    remove_and_merge_bad_lines(page, kv_pairs, header_lines, page_number)

    print("\n\n----\n\n")
    print("Cleaned lines:")
    for line in page.lines:
        print(line.text)

if __name__ == "__main__":
    document = Document.open("textractJson.json")
    pre_process_page(document, PAGE_NUMBER, HEADER_LINES)
