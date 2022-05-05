import subprocess
import sys

words = sys.argv[1:]
sentence = "%20".join(words)
sentence = sentence.replace(" ", "%20")

cmd = (
    f"curl -s -o /dev/null "
    f'"https://maker.ifttt.com/trigger/notify/with/key/$IFTTT_KEY?value1={sentence}"'
)

subprocess.check_call(cmd, shell=True)
print(f"Push notification <{sentence.replace('%20', ' ')}> sent to app.")
