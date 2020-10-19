"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

Minimum Edit Distance Dynamic Programming
https://www.youtube.com/watch?v=We3YDTzNXEk&list=PLrmLmBdmIlpsHaNTPP_jHHDx_os9ItYXr&index=6

Suppose your rows represents str1, cols represents str2. If you wanna delete, you go back to previous column, which is T[i][j-1], because you'd like to retrieve the last character in str2. Similarly, if you wanna insert, you go back to previous row, which is T[i-1][j]. For replacing current character, you need to retrieve last character in both str1 and str2, which is T[i-1][j-1]. At last, you get the minimum among the above 3 moves and plus 1 to it to get T[i][j].

"""
import numpy
import fire


def get_word_error_rate(r, h):

    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    result = float(d[len(r)][len(h)]) / len(r) * 100

    return result, d


def print_to_html(r, h, d, fn):
    x = len(r)
    y = len(h)

    html = (
        '<html><body><head><meta charset="utf-8"></head>'
        "<style>.g{background-color:#0080004d}.r{background-color:#ff00004d}.y{background-color:#ffa50099}</style>"
    )

    while True:
        if x == 0 or y == 0:
            break

        if r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            html = "%s " % h[y] + html
        elif d[x][y] == d[x - 1][y - 1] + 1:  # substitution
            x = x - 1
            y = y - 1
            html = '<span class="y">%s(%s)</span> ' % (h[y], r[x]) + html
        elif d[x][y] == d[x - 1][y] + 1:  # deletion
            x = x - 1
            html = '<span class="r">%s</span> ' % r[x] + html
        elif d[x][y] == d[x][y - 1] + 1:  # insertion
            y = y - 1
            html = '<span class="g">%s</span> ' % h[y] + html
        else:
            print("\nWe got an error.")
            break

    html += "</body></html>"

    with open(fn, "w") as f:
        f.write(html)
    f.close()
    print("Printed comparison to: {0}".format(fn))


def main(ground_truth, candidate, filter_punc, drop_stopgap, suffix):
    gt = open(ground_truth).read()[:-1]
    c = open(candidate).read()[:-1]
    if filter_punc.lower() == "true":
        gt = gt.lower()
        c = c.lower()
        for p in [",", ".", "?", "!", "*"]:
            gt = gt.replace(p, "")
            c = c.replace(p, "")
    if drop_stopgap.lower() == "true":
        for p in ["uh", "um"]:
            gt = gt.replace(f" {p} " , " ")
            c = c.replace(f" {p} " , " ")
    wer, d = get_word_error_rate(gt.split(), c.split())
    fn = f"comparison_{suffix}.html"
    print(f"{suffix} wer: {wer}")
    print_to_html(gt.split(), c.split(), d, fn)


if __name__ == "__main__":
    fire.Fire(main)
